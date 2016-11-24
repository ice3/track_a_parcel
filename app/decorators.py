"""Decorators to use in the app."""
from threading import Thread


def async(f):
    """Decorator to make an asynchrone call to a function.

    The function is launched is a subthread.
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
