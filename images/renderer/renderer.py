from werkzeug.wrappers import Request, Response
from nbconvert.exporters import HTMLExporter

import os
import stat
import markdown
import docutils.core

BASE_PATH = os.environ["BASE_PATH"]
URL_PREFIX = os.environ["URL_PREFIX"]
REAL_BASE_PATH = os.path.realpath(BASE_PATH)

# Users control the content of rst files. Do not let directives such as
# include, raw or csv-table read files from the renderer filesystem.
# Do not let docutils config files change these settings.
RST_SETTINGS = {
    "file_insertion_enabled": False,
    "raw_enabled": False,
    "_disable_config": True,
}


def get_extension(path, format):
    """
    Return the extension of the path, if any
    """
    splits = path.split(".")
    if len(splits) == 1:
        # This means there's no two parts - so either no ., or nothing before
        # or after the .. Easier to handle by just saying we found no extensions
        return ""
    return splits[-1]


def is_allowed_path(real_path):
    """
    Return True if a resolved path is in BASE_PATH and is not hidden.
    nginx does not serve dotfiles, thus the renderer must not render them.
    """
    if os.path.commonpath([REAL_BASE_PATH, real_path]) != REAL_BASE_PATH:
        return False
    relative_path = os.path.relpath(real_path, REAL_BASE_PATH)
    return not any(part.startswith(".") for part in relative_path.split(os.sep))


def open_file(file_path):
    """
    Open a regular file in BASE_PATH and return a text file object.

    Check the path of the open file descriptor, not the requested path.
    Thus a user cannot change a symlink after the check to read a different
    file. O_NONBLOCK prevents a block on a FIFO.
    """
    fd = os.open(
        os.path.join(BASE_PATH, file_path), os.O_RDONLY | os.O_NONBLOCK
    )
    try:
        real_path = os.readlink("/proc/self/fd/%d" % fd)
        if not stat.S_ISREG(os.fstat(fd).st_mode) or not is_allowed_path(
            real_path
        ):
            raise PermissionError(file_path)
        return open(fd, encoding="utf-8")
    except BaseException:
        os.close(fd)
        raise


def render_ipynb(file_handle, format):
    """
    Render a given ipynb file
    """
    exporter = HTMLExporter()
    html, _ = exporter.from_file(file_handle)
    return Response(html, mimetype="text/html")


def render_md(file_handle, format):
    """
    Render a given markdown file
    """
    html = markdown.markdown(file_handle.read())
    return Response(html, mimetype="text/html")


def render_rst(file_handle, format):
    """
    Render a given reStructuredText file
    """
    html = docutils.core.publish_string(
        source=file_handle.read(),
        writer_name="html",
        settings_overrides=RST_SETTINGS,
    )
    return Response(html, mimetype="text/html")


# Map of extensions to functions to call for handling them
handlers = {
    "rst": render_rst,
    "md": render_md,
    "ipynb": render_ipynb,
}


@Request.application
def application(request):
    file_path = request.path.lstrip(URL_PREFIX)
    format = request.args.get("format", None)
    try:
        if format == "raw":
            # Let nginx serve raw files
            with open_file(file_path):
                pass
            accel_path = os.path.join("/accelredir/", file_path)
            return Response("", headers={"X-Accel-Redirect": accel_path})

        extension = get_extension(file_path, format)
        if extension and extension in handlers:
            with open_file(file_path) as file_handle:
                return handlers[extension](file_handle, format)
        else:
            return Response("No handlers for format %s" % extension, status=400)
    except FileNotFoundError:
        return Response("Not found", status=404)
    except PermissionError:
        return Response("Forbidden", status=403)


if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 4000, application)
