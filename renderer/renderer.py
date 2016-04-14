from werkzeug.wrappers import Request, Response
from nbconvert.exporters import HTMLExporter

import os

BASE_PATH = os.environ['BASE_PATH']
URL_PREFIX = os.environ['URL_PREFIX']

@Request.application
def application(request):
    full_path = os.path.join(BASE_PATH, request.path.lstrip(URL_PREFIX))
    # Protect against path traversal attacks, if they make it this far.
    if not full_path.startswith(BASE_PATH):
        # DANGER!
        return Response("Suspicious url", status=403)
    if full_path.endswith('.ipynb'):
        exporter = HTMLExporter()
        with open(full_path) as file_handle:
            html, res = exporter.from_file(file_handle)
            return Response(html, mimetype='text/html')
    return Response(full_path)
