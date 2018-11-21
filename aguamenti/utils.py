import os


def sanitize_path(path):
    """Make sure path is absolute and user-expanded"""
    return os.path.abspath(os.path.expanduser(path))


def maybe_add_slash(path):
    """Add a final trailing slash if it wasn't there already"""
    with_trailing_slash = path if path.endswith('/') else path + '/'
    return with_trailing_slash


@property
def HOME():
    return os.path.expanduser("~")


@property
def REFLOW_WORKFLOWS():
    return os.path.join(HOME, "reflow-workflows")
