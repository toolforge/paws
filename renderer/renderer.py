from werkzeug.wrappers import Request, Response
from nbconvert.exporters import HTMLExporter

import os

BASE_PATH = os.environ['BASE_PATH']
URL_PREFIX = os.environ['URL_PREFIX']

def get_extension(path):
    """
    Return the extension of the path, if any
    """
    splits = path.split('.')
    if len(splits) == 1:
        # This means there's no two parts - so either no ., or nothing before
        # or after the .. Easier to handle by just saying we found no extensions.
        return ''
    return splits[-1]

def render_ipynb(full_path):
    """
    Render a given ipynb file
    """
    exporter = HTMLExporter()
    with open(full_path, encoding='utf-8') as file_handle:
        html, res = exporter.from_file(file_handle)
    return Response(html, mimetype='text/html')

# Map of extensions to functions to call for handling them
handlers = {
    'ipynb': render_ipynb,
}

@Request.application
def application(request):
    file_path = request.path.lstrip(URL_PREFIX) 
    full_path = os.path.join(BASE_PATH, file_path)
    # Protect against path traversal attacks, if they make it this far.
    if not full_path.startswith(BASE_PATH):
        # DANGER!
        return Response("Suspicious url", status=403)
    if request.args.get('format', None) == 'raw':
        accel_path = os.path.join('/accelredir/', file_path)
        return Response('', headers={'X-Accel-Redirect': accel_path})

    try:
        extension = get_extension(full_path)
        if extension:
            return handlers[extension](full_path)
    except FileNotFoundError:
        return Response("Not found", status=404)
    return Response(full_path)
