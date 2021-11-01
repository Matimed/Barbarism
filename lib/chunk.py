from lib.abstract_data_types import Matrix
from lib.position import Position


class Chunk:
    """ A matrix of Positions used to 
        render the world in separate parts.
    """

    def __init__(self, positions:Matrix, index:tuple[int, int]):
        self.positions = positions
        self.index = index

    
    def get_corner(self) -> list[Position, Position]:
        """ Returns the position of the upper left corner and 
            the lower right corner.
        """

        corners = list()

        corners.append(self.position.get_element((0,0)))
        corners.append(self.position.get_element(positions.length()))

        return corners

    
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


    def verify_area(self, position, area:tuple[int,int]) -> Matrix:
        """ Receives a Position and returns a Matrix that indicates 
            if the Chunk has the positions around it in the given area, 
            indicating it with a boolean in each position.
            The area must be a tuple of the length of the expected matrix.
        """

        assert self.has(position), \
            "The position doesn't belong to the chunk."

        
        y_distance = (area[0]-1)//2
        x_distance = (area[1]-1)//2
        
        origin = list(self.positions.index(position))
        origin[0] = origin[0] - y_distance
        origin[1] = origin[1] - x_distance

        verify_matrix = Matrix()
        for row in range (origin[0], area[0]+origin[0]):
            verify_row = []
            for column in range(origin[1], area[1]+origin[1]):
                try:
                    self.positions.get_element((row,column))
                    verify_row.append((True,row,column))
                except:
                    verify_row.append((False,row,column))
            verify_matrix.append_row(verify_row)

        return verify_matrix


    def get_random_position(self):
        """ Returns a random position.
        """

        return self.positions.random()


    def __iter__(self):
        return self.positions.__iter__()

