import os

mylang = 'test'
family = 'wikipedia'


# Not defining any extra variables here at all since that causes pywikibot
# to issue a warning about potential misspellings
if os.path.exists(os.path.expanduser('~/user-config.py')):
    with open(os.path.expanduser('~/user-config.py'), 'r') as f:
        exec(
             compile(f.read(), os.path.expanduser('~/user-config.py'), 'exec'),
             globals())

# Things that should be non-easily-overridable
usernames['*']['*'] = os.environ['JPY_USER']
