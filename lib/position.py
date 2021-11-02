from functools import singledispatchmethod


class Position:
    """ Coordanates system that uses an 'y' and 'x' notation 
        to represent unequivocally a specific location that goes 
        universally for every object.
    """

    def __init__(self, y:int, x:int):

        self._format_verification(y, x)
        
        self.y = y
        self.x = x


    def get_index(self):
        return (self.y, self.x)


    @singledispatchmethod
    def __eq__(self, other):
        """ Uses the get_index method to equalize 
            both instannces of position
        """

        try:
            other_get_index= other.get_index
        except AttributeError:
            return False

        return self.get_index() == other_get_index()


    @__eq__.register(tuple)
    def _(self, other):
        """ Uses get_index method to equalize an instance 
            of position with a tuple.
        """

        assert len(other) == 2, ("Tuple that went through a parameter" 
            + "must contain two elements.")

        self._format_verification(other[0], other[1])

        return (other[0], other[1]) == self.get_index()


    def __hash__(self):
        return hash((self.y, self.x))


    def _format_verification(self, y, x):
        assert type(y) == int, "'y' must be an int."
        assert type(x) == int, "'x' must be an int."


    def __repr__(self):
        return f"({self.y}, {self.x})"