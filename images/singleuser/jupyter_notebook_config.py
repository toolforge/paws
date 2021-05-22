# Disable flake8 for this file, since it's a config file not just python
# flake8: noqa
import os

openrefine_path = os.path.join(os.environ['OPENREFINE_DIR'], 'refine')
openrefine_logo_path = os.path.join(os.environ['OPENREFINE_DIR'], 'openrefine-logo.svg')
c.ServerProxy.servers = {
    'openrefine': {
        'command': [openrefine_path, '-p', '{port}', '-d', os.path.expanduser('~')],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': openrefine_logo_path,
            'title': 'OpenRefine',
        },
    },
}