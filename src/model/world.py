from model.cells.plain import Plain
from position import Position


class World:
    def __init__(self, order = 11):
        self.positions = self._generate_positions(order)
        self.cells = self._generate_cells(self.positions)


    def create_route(self, origin, destination):
        """ Given two Position returns the fastest way
            to get from the origin to the destination point.
        """

        raise NotImplementedError

    
    def _generate_positions(self, order):
        matrix = []
        for x in range(1, order):
            row_list = []
            
            for y in range(1, order):
                row_list.append(Position(x,y))
            
            matrix.append(row_list)

        return matrix

    
    def _generate_cells(self, positions):
        cells = {}
        for row in positions:
            for position in row:
                # Cells should be random and not all Plain.
                cells[position] = Plain()
        
        return cells