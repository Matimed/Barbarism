from lib.abstract_data_types import Matrix
from lib.position import Position


class Chunk:
    """ A matrix of Positions used to 
        render the world in separate parts.
    """

    def __init__(self, positions:Matrix, index:tuple[int, int]):
        self.positions = positions
        self.index = index

    
    def greater_than(self, chunk) -> tuple[bool, bool]:
        """ Compares the index with another chunk to know
            which one is prior to the other and returns a tuple 
            that indicates True if the current chunk is grather
            than the one passed by parameter.
        """

        assert self.index != chunk.get_index(), \
            "Cannot compare with the same chunk."

        y = self.index[0] > chunk.get_index()[0]
        x = self.index[1] > chunk.get_index()[1]

        return (y, x)

    
    def get_index(self) -> tuple[int, int]:
        """ Returns the chunk index.
        """

        return self.index


    def get_position_index(self, position):
        return self.positions.index(position)

    
    def get_row(self, index: int) -> list:
        """ If it has the row of the requested index it is returned 
            and if not, it returns False. 
        """

        if not (index >= self.position.length[0] or index <= 0):
            return self.positions.get_row(index)

        else:
            return False

    
    def has(self, position) -> bool:
        """ Returns a boolean that indicates 
            if the position is in the Chunk.
        """

        return bool(self.positions.index(position)) 


    def get_element(self, index: int) -> tuple:
        """ If it has the element of the requested index it is returned 
            and if not, it returns False. 
        """

        if not (index >= self.position.length[0] or index <= 0):
            return self.positions.get_element(index)
        
        else:
            return False


    def get_column(self, index: int) -> tuple:
        """ If it has the column of the requested index it is returned 
            and if not, it returns False. 
        """

        if not (index >= self.position.length[1] or index <= 0):
            return self.positions.get_column(index)

        else: 
            return False


    def length(self)-> tuple[int, int]:
        """ Returns a tuple that represent the size of the chunk 
            (number of rows, number of columns).
        """

        return self.positions.length()


    def copy_matrix(self) -> Matrix:
        """ Returns a copy of the positions Matrix that contains.
        """

        return self.positions.copy()


    def verify_area(self, origin:Position, area: tuple[int,int]) -> Matrix:
        """ Receives a center position and returns a Matrix that contains
            all the positions around that are in the Chunk.
            The area must be a tuple of the expected array length.
        """

        assert self.has(origin), \
            "The position doesn't belong to the chunk."

        origin = list(self.positions.index(origin))
        verify_matrix = Matrix()
        for row in range (origin[0], area[0]+origin[0]):
            verify_row = []
            
            for column in range(origin[1], area[1]+origin[1]):
                try:
                    verify_row.append((self, self.positions.get_element((row,column))))

                except AssertionError:
                    continue
            
            if verify_row: verify_matrix.append_row(verify_row)
            

        return verify_matrix


    def get_random_position(self):
        """ Returns a random position.
        """

        return self.positions.random()


    def __iter__(self):
        return self.positions.__iter__()

