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
        cells = self.cells

        first_cell = cells[0][0]
        first_cell.rect.topleft = self.origin
        for row in range(len(cells)):
            if row != 0:
                current_cell = cells[row][0]
                previous_cell = cells[row - 1][0]

                current_cell.rect.midtop = previous_cell.rect.midbottom
                current_cell.draw(surface)

            for column in range(row):
                if column != 0:
                    current_cell = cells[row][column]
                    previous_cell = cells[row][column - 1]

                    current_cell.rect.midleft = previous_cell.rect.midright
                    current_cell.draw(surface)

