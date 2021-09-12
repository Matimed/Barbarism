from functools import singledispatchmethod


class Position:
    """ Coordanates system that uses an 'x' and 'y' notation 
        to represent unequivocally a specific location that goes 
        universally for every object.
    """

    def __init__(self, x, y):
        """ Recives:
                x:<int>
                y:<int>
        """

        self._format_verification(x, y)
        
        self.x = x
        self.y = y


    def get_position(self):
        return self.x, self.y


    @singledispatchmethod
    def __eq__(self, other):
        """ Uses the get_position method to equalize 
            both instannces of position
        """

        try:
            other_get_position = other.get_position
        except AttributeError:
            raise NotImplementedError()

        return self.get_position() == other_get_position()


    @__eq__.register(tuple)
    def _(self, other):
        """ Uses get_position method to equalize an instance 
            of position with a tuple.
        """

        assert len(other) == 2, ("Tuple that went through a parameter" 
            + "must contain two elements.")

        self._format_verification(other[0], other[1])

        return (other[0], other[1]) == self.get_position()


    def __hash__(self):
        return hash((self.x, self.y))


    def _format_verification(self, x, y):
        assert type(x) == int, "'x' must be an int."
        assert type(y) == int, "'y' must be an int."


    def __repr__(self):
        return f"({self.x}, {self.y})"