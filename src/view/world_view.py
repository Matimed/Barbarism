from pygame.sprite import AbstractGroup
from src.view.sprites import CellSprite


class WorldView(AbstractGroup):
    def __init__(self, event_dispatcher, world, window, origin = (0,0)):
        CellSprite.set_event_dispatcher(event_dispatcher)
        
        self.world = world
        self.window = window
        self.world.generate_chunks(self.get_chunk_size())

        self.cells = self._generate_cells(world.get_positions())
        self.origin = origin


    def get_chunk_size(self) -> int:
        """ Returns the number of cells that fit in a chunk.
        """
        
        max_resolution = self.window.get_resolution()
        cell_min_size = CellSprite.get_min_size()
        cells_max_width = max_resolution[0] // cell_min_size
        cells_max_height = max_resolution[1] // cell_min_size

        return max(cells_max_width, cells_max_height)


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
