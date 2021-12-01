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


    def __eq__(self, other):
        try:
            return self._func == other.__func__ and self._self == weakref.ref(other.__self__)
        except:
            return self._func == other._func and self._self == other._self


    def __bool__(self):
        return self._self() is not None