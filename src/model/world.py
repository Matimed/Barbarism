from src.model.cells import Plain
from lib.position import Position
from lib.abstract_data_types import Matrix


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """

    def __init__(self, order = 11):
        self.positions = self._generate_positions(order)
        self.cells = self._generate_cells(self.positions)


    def create_route(self, origin, destination):
        """ Given two Position returns the fastest way
            to get from the origin to the destination point.
        """

        raise NotImplementedError

    
    def _generate_positions(self, order):
        """ Generates a Matrix of Position type objects 
            based on the given size (order).
        """

        positions = Matrix()

        for y in range(order):
            row_positions = []
            
            for x in range(order):
                row_positions.append(Position(y, x))
            
            positions.append_row(row_positions)

        return positions

    
    def _generate_cells(self, positions):
        """ Recives a Matrix of Position type objects and
            generate a dict of Cell type objects with a position as key.
        """
        
        cells = {}

        for i in positions:
            cells[i] = Plain()

        return cells


    def get_positions(self):
        return self.positions

    
    def get_biomes(self):
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """

        raise NotImplementedError
    
    
