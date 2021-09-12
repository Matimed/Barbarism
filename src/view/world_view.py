from pygame.sprite import AbstractGroup
from view.sprites.cell_sprite import CellSprite


class WorldView(AbstractGroup):
    def __init__(self, positions, origin = (0,0)):
        self.cells = self._generate_cells(positions)
        self.origin = origin


    def draw(self, surface):
        self._draw_cells(surface)


    def _generate_cells(self, positions):
        """ Generates a CellSprite for each Position 
            in positions (two-dimensional Position array) 
            and returns a two-dimensional CellSprite array.
        """

        cells = []
        for row in positions:
            rowlist = []

            for position in row:
                cell = CellSprite(position)
                rowlist.append(cell)
            
            cells.append(rowlist)

        return cells


    def _change_cell_biome(self, biomes):
        """ Recives a dict of cell biome with a Position as key
            and change the image of each CellSprite in self.cells
            to the correct biome.
        """

        raise NotImplementedError


    def _draw_cells(self, surface):
        """ Draws all the cells in order into a surface."""
        
        cell_origin = self.origin
        
        for y ,row in enumerate(self.cells):
            for cell in row:
                cell.rect.topleft = cell_origin
                cell_origin = cell.rect.topright

                cell.draw(surface)

            cell_origin = self.cells[y][0].rect.bottomleft