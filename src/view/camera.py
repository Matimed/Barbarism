from src.view.sprites import CellSprite
from src.events import Tick
from src.events import Wheel
from src.events import CellPressed
from lib.abstract_data_types import Matrix
from src.events import Click


class Camera:
    def __init__(self, event_dispatcher, window, world_view):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.draw)
        self.ed.add(Wheel, self.zoom)

        self.window = window

        self.world_view = world_view

        self.visible_cells = Matrix()
        self.visible_chunks = set()

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
                cell[1].rect.topleft = previous_point
                previous_point = cell[1].rect.topright
                cell[1].draw(self.window.get_surface())
            
            previous_point = row[0][1].rect.bottomleft
            

    def zoom(self, event):
        """ Receive the Wheel event and create the illusion of getting
            closer to the map by changing the CellSprites size and quantity.
        """

        cell_sized = (
            CellSprite.get_actual_size() + (event.get_movement() * 2)
            )

        if cell_sized > CellSprite.get_min_size():
            CellSprite.set_size(cell_sized)

            if event.get_movement() == 1:
                if not (self.visible_cells.length()[0] <= 4 or self.visible_cells.length()[1] <= 4): 
                    self.zoom_in(self._calculate_length(CellSprite.get_actual_size()))


    def zoom_in(self, desired_size):
        """ Deletes cells of the visible_cells Matrix until the quatity of 
            cells be equal to the desired size passed by argument.
            Also desubscribes the deleted cells from the Click event.
        """

        actual_size = self.visible_cells.length()
        
        switch = 0 # switch value can be 0 or -1
        for x in range(actual_size[0] - desired_size[0]):
            row = self.visible_cells.pop_row(switch)

            for element in row:
                self.ed.remove(Click, element[1].handle_collisions)

            switch = (not (switch + 1)) - 1

        for x in range(actual_size[1] - desired_size[1]):
            column = self.visible_cells.pop_column(switch)

            for element in column:
                self.ed.remove(Click, element[1].handle_collisions)

            switch = (not (switch + 1)) - 1
        
        self.refresh_cells()
        self.origin = self._get_new_origin()


    def refresh_cells(self):
        """ Executes the refresh method of all cells in the visible 
            cells Matrix in order to change they size.
        """

        for cell in self.visible_cells:
            cell[1].refresh()


    def point(self, chunk, position):
        """ Receives a Position and its Chunk and centers them on screen.
        """

        actual_length = self._calculate_length(CellSprite.get_actual_size())

        positions = self.world_view.get_positions_around(position, actual_length)
        chunks = set([chunk[0] for chunk in positions])
        for chunk in chunks:
            self.world_view.render_adjacent_chunks(self, chunk)

        self.set_visible_chunks(chunks)
        self.set_visible_cells(self.world_view.get_cells(positions))


    def set_visible_chunks(self, chunks):
        """ Replace the list of visible chunks for a new one. 
        """
        
        self.visible_chunks = chunks


    def set_visible_cells(self, cells):
        """ Replace the Matrix of visible cells for a new one,
            recalculates the origin point and subscribes the 
            cells to the Click event.
        """
        
        for cell in self.visible_cells:
            self.ed.remove(Click, cell[1].handle_collisions)
        
        for cell in cells:
            self.ed.add(Click, cell[1].handle_collisions)

        self.visible_cells = cells
        self.origin = self._get_new_origin()


    def _get_new_origin(self):
        """ Calculates and returns the point 
            from which the cells should be drawn,
            based on the resolution, the zoom and the matrix length.
        """

        resolution = self.window.get_resolution()
        cell_size = CellSprite.get_actual_size()
        length = self.visible_cells.length()

        margins = (
            resolution[0] - (length[1] * cell_size),
            resolution[1] - (length[0] * cell_size)
            )

        origin = (margins[0] // 2, margins[1] // 2)        

        return origin


    def _calculate_length(self, cells_size:int) -> tuple[int, int]:
        """ Returns the length that the visible_cells should have,
            based on the given size of the CellSprites.
        """

        resolution = self.window.get_resolution()

        return (resolution[1] // cells_size, resolution[0] // cells_size)

