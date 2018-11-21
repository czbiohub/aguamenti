import os


unicode_usa = 'en_US.utf-8'
os.environ['LC_LANG'] = unicode_usa
os.environ["LC_ALL"] = unicode_usa

HOME = os.path.expanduser("~")
REFLOW_WORKFLOWS = os.path.join(HOME, "reflow-workflows")


def sanitize_path(path):
    """Make sure path is absolute and user-expanded"""
    return os.path.abspath(os.path.expanduser(path))


def maybe_add_slash(path):
    """Add a final trailing slash if it wasn't there already"""
    with_trailing_slash = path if path.endswith('/') else path + '/'
    return with_trailing_slash
