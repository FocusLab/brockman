class BadAPIKey(Exception):
    "The API key you provided was rejected."

class BadRequest(Exception):
    "The FocusLab rejected the request because it wasn't properly formed"

class ResourceNotFound(Exception):
    """
    FocusLab returned a 404.  This probably means that you have a problem
    with your endpoint or resource name.
    """

class ServerError(Exception):
    """
    It looks like there's a problem with the FocusLab service.  Try the request
    again in a few minutes or report the problem to FocusLab.
    """

class UnknownError(Exception):
    "FocusLab returned an unexpected status code.  Please report this problem."
