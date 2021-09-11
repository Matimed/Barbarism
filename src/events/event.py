from aenum import Enum
from functools import singledispatchmethod


class Event(Enum):
    """ An enumeration of event types that allows 
        to document the arguments that recives.
    """
    
    
    def __init__(self, val, *args):
        """ Cumple la funcion de separar el val del event 
            y la documentacion del mismo.
        """

        self.val = val
        if args:
            self.__doc__ = "Argumentos:"
            for arg in args:
                self.__doc__ += f" {arg},"
            self.__doc__ = self.__doc__[:-1]
        else:
            self.__doc__ = "No recibe argumentos"


    @singledispatchmethod
    def __eq__(self, other):
        """ Compare two events"""

        try:    return self.val == other.val
        except AttributeError:  raise NotImplementedError()


    @__eq__.register(int)
    def _(self, other):
        """ Compare an event with an int"""
        
        return self.val == other