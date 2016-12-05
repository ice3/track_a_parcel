"""Decorators to use in the app."""
from threading import Thread
from flask import request, Response
from functools import wraps


def async(f):
    """Decorator to make an asynchrone call to a function.

    The function is launched is a subthread.
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def check_auth(username, password):
    """Check if a username / password combination is valid."""
    return username == 'harry' and password == 'ormistyrat'


def authenticate():
    """Send a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    """Check if the auth tokens are correct.

    source: http://flask.pocoo.org/snippets/8/
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
