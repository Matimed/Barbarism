from lib.abstract_data_types import Matrix
from lib.position import Position


class Chunk:
    """ A matrix of Positions used to 
        render the world in separate parts.
    """

    def __init__(self, positions, index):
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
        assert self.index != chunk.get_index(), \
            "Cannot compare with the same chunk."

        x = self.index[0] > chunk.get_index()[0]
        y = self.index[1] > chunk.get_index()[1]

        return (x, y)

    
    def get_index(self) -> tuple[int, int]:
        """
        """

        return self.index

    
    def get_row(self, index: int) -> tuple:
        if not (index >= self.position.length[0] or index <= 0):
            return self.positions.get_row(index)

        else:
            return False


    def get_column(self, index: int) -> tuple:
        if not (index >= self.position.length[1] or index <= 0):
            return self.positions.get_column(index)

        else: 
            return False