from pygame.sprite import AbstractGroup
from src.view.sprites import CellSprite


class WorldView(AbstractGroup):
    def __init__(self, event_dispatcher, positions, origin = (0,0)):
        CellSprite.set_event_dispatcher(event_dispatcher)
        
        self.cells = self._generate_cells(positions)
        self.origin = origin


    def _generate_cells(self, positions):
        """ Generates a CellSprite for each Position 
            in positions (Matrix of Position objects) 
            and returns a Matrix of CellSprite objects.
        """

        cells = positions.copy()
        for position in cells:
            cells.set_element(cells.index(position), CellSprite(position))

        return cells


    def _asign_biomes(self, biomes):
        """ Recives a dict of cell biomes with a Position as key
            and change the image of each CellSprite in self.cells
            to the correct biome.
        """

        raise NotImplementedError


    def draw(self, surface):
        """
        """

        self.__draw_cells(surface)



    def __draw_cells(self, surface):
        """ Draws all the cells in order into a surface.
        """
        
        previous_point = (self.origin)
        for row in self.cells.iter_rows():
            for cell in row:

                # We know that we are breaking OOP paradim
                # when we access an argument directly but 
                # this is neccesary because pygame does not have 
                # a suitable method of accessing the rect attributes.

                cell.rect.topleft = previous_point
                previous_point = cell.rect.topright
                cell.draw(surface)
            
            previous_point = row[0].rect.bottomleft
