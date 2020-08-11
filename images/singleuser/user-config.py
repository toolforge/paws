import os

mylang = "test"
family = "wikipedia"

if "usernames" not in globals():
    usernames = {}

if "authenticate" not in globals():
    authenticate = {}

custom_path = os.path.expanduser("~/user-config.py")
if os.path.exists(custom_path):
    with open(custom_path, "rb") as f:
        exec(compile(f.read(), custom_path, "exec"), globals())

    del f
# Clean up temp variables, since pwb issues a warning otherwise
# to help people catch misspelt config
del custom_path

# Things that should be non-easily-overridable
for fam in (
    "wikipedia",
    "commons",
    "meta",
    "wikibooks",
    "wikimedia",
    "wikiquote",
    "wikisource",
    "wikisource",
    "wiktionary",
    "wikiversity",
    "wikidata",
    "mediawiki",
    "wikivoyage",
    "wikinews",
):
    usernames[fam]["*"] = os.environ["USER"]

del fam

# If OAuth integration is available, take it
if "CLIENT_ID" in os.environ:
    authenticate["*"] = (
        os.environ["CLIENT_ID"],
        os.environ["CLIENT_SECRET"],
        os.environ["ACCESS_KEY"],
        os.environ["ACCESS_SECRET"],
    )
