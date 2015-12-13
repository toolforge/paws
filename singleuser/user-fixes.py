import os

custom_path = os.path.expanduser('~/user-fixes.py')
if os.path.exists(custom_path):
    with open(custom_path, 'rb') as f:
        exec(compile(f.read(), custom_path, 'exec'), globals())

    del f

# Clean up temp variables, since pwb issues a warning otherwise
# to help people catch misspelt config
del custom_path
