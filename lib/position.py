

class Position:
    """ Coordanates system that uses an 'y' and 'x' notation 
        to represent unequivocally a specific location that goes 
        universally for every object.
    """

    __slots__ = ('y', 'x')

    @staticmethod
    def create_collection(first_position: tuple, last_position: tuple):
        """ Generates the postions between the passed two position index.
        """
        
        assert type(last_position[0]) == int and type(first_position[0]) == int, \
            "'y' must be an int."

        assert type(first_position[1]) == int and type(last_position[1]) == int, \
            "'x' must be an int."

        return [[Position(y, x) 
            for x in range(first_position[1], last_position[1] + 1)]
                for y in range(first_position[0], last_position[0] + 1)]
    

    def __init__(self, y:int, x:int):
        self.y = y
        self.x = x


    def get_index(self):
        return (self.y, self.x)


    def __hash__(self): return hash((self.y, self.x))


    def __repr__(self): return f"({self.y}, {self.x})"


    def __getitem__(self, i): return list(self.get_index())[i]


    def __eq__(self, other):
        """ Uses the get_index method to equalize 
            both instannces of position
        """

        try:
            other_get_index = other.get_index
        except AttributeError:
            return False

        return self.get_index() == other_get_index()
