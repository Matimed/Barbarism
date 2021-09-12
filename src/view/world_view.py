from pygame.sprite import AbstractGroup
from view.sprites.cell_sprite import CellSprite


class WorldView(AbstractGroup):
    def __init__(self):
        self.cells = self._generate_cells()

    
    def _generate_cells(self, positions):
        """ Generates a cell for each position.
        
            Receives:
                positions:<array> 2D

            Returns:
                cells:<array> 2D
        """

        cells = []
        for row in positions:
            rowlist = []

            for position in row:
                cell = CellSprite(position)
                rowlist.append(cell)
            
            cells.append(rowlist)

        return cells