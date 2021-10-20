import weakref


class WeakBoundMethod:
    """ Converts a bound method instance 
        of a class into a weak reference.
    """

    def __init__(self, meth):
        self._self = weakref.ref(meth.__self__)
        self._func = meth.__func__


    def __call__(self, *args, **kwargs):
        self._func(self._self(), *args, **kwargs)