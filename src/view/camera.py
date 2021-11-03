from src.view.sprites import CellSprite
from src.events import Tick
from lib.abstract_data_types import Matrix


class Camera:
    def __init__(self, event_dispatcher, window, world_view):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.draw)

        self.window = window

        self.world_view = world_view

        self.visible_cells = Matrix()
        self.visible_chunks = list()


        self.origin = (0,0)

        # Minimum harcoded size for the cells matrix. 
        self.min_length = (5,3)
        self.max_length = self._calculate_length(CellSprite.get_min_size())



    def draw(self, event):
        """ Loops through the Matrix of visible cells and draw them. 
        """

        previous_point = self.origin

        for row in self.visible_cells.iter_rows():
            for cell in row:

                # We know that we are breaking OOP paradim
                # when we access an argument directly but 
                # this is neccesary because pygame does not have 
                # a suitable method of accessing the rect attributes.
                cell.rect.topleft = previous_point
                previous_point = cell.rect.topright
                cell.draw(self.window.get_surface())
            
            previous_point = row[0].rect.bottomleft


    def point(self, chunk, position):
        """ Receives a Position and its Chunk and centers them on screen.
        """

        self.set_visible_chunks(chunk)
        actual_length = self._calculate_length(CellSprite.get_actual_size())

        positions = self.world_view.get_positions_around(position, actual_length)
        chunks = set([chunk[0] for chunk in positions])
        for chunk in chunks:
            self.world_view.render_adjacent_chunks(self, chunk)
        self.set_visible_cells(self.world_view.get_cells(positions))


    def set_visible_chunks(self, chunks):
        """ Replace the list of visible chunks for a new one. 
        """
        
        self.visible_chunks = chunks


    def set_visible_cells(self, cells):
        """ Replace the Matrix of visible cells for a new one 
            and recalculates the origin point.
        """

        self.visible_cells = cells
        self.origin = self._get_new_origin()


    def _get_new_origin(self):
        """ Calculates and returns the point 
            from which the cells should be drawn,
            based on the resolution, the zoom and the matrix length.
        """

        resolution = self.window.get_resolution()
        cell_size = CellSprite.get_actual_size()
        lenght = self.visible_cells.length()

        margins = (
            resolution[0] - (lenght[0] * cell_size),
            resolution[1] - (lenght[1] * cell_size)
            )

        origin = (margins[0] // 2, margins[1] // 2)        

        return origin


    def _calculate_length(self, cells_size:int ) -> tuple[tuple, tuple]:
        """ Returns the length that the visible_cells should have,
            based on the given size of the CellSprites.
        """

        resolution = self.window.get_resolution()

        return (resolution[0] // cells_size, resolution[1] // cells_size)
