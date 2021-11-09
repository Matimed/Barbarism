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

        self._switch = 0

        # Minimum harcoded size for the cells matrix. 
        self.min_length = (3,5)
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

        new_size = (
            CellSprite.get_actual_size() + (event.get_movement() * 2)
            )

        if new_size > CellSprite.get_min_size():
            desired_length = self._calculate_length(new_size)

                
            if (
                event.get_movement() == 1 and 
                desired_length[0] >= self.min_length[0] and
                desired_length[1] >= self.min_length[1]
                ):
                
                CellSprite.set_size(new_size)
                self.zoom_in(desired_length)

            elif (
                event.get_movement() == -1 and
                desired_length[0] <= self.max_length[0] and
                desired_length[1] <= self.max_length[1]
                ):
                
                CellSprite.set_size(new_size)
                self.zoom_out(desired_length)
            
            self.refresh_cells()
            self.origin = self._get_new_origin()


    def zoom_in(self, desired_size):
        """ Deletes cells of the visible_cells Matrix until the quatity of 
            cells be equal to the desired size passed by argument.
            Also desubscribes the deleted cells from the Click event.
        """

        actual_size = self.visible_cells.length()
        
        for i in range(actual_size[0] - desired_size[0]):
            row = self.visible_cells.pop_row(-(self._switch))

            for element in row:
                self.ed.remove(Click, element[1].handle_collisions)

            self._switch = not self._switch

        for i in range(actual_size[1] - desired_size[1]):
            column = self.visible_cells.pop_column(-self._switch)

            for element in column:
                self.ed.remove(Click, element[1].handle_collisions)

            self._switch = not self._switch


    def zoom_out(self, desired_size):
        actual_size = self.visible_cells.length()
        for axis in [0,1]:
            for i in range(desired_size[axis] - actual_size[axis]):

                new_collection = None
                while bool(new_collection) == False:
                    if axis:
                        cells = self.visible_cells.get_column(-self._switch)
                    else:
                        cells = self.visible_cells.get_row(-self._switch)

                    collection = [
                        (element[0], element[1].get_position()) for element in cells
                        ]

                    if self._switch:
                        new_collection = self.world_view._find_parallel_collection(collection, not axis, 1)
                    else:
                        new_collection = self.world_view._find_parallel_collection(collection, not axis, -1)

                    if new_collection == None: self._switch = not self._switch


                cells = self.world_view.get_cells_by_list(new_collection)
                for cell in cells:
                    self.ed.add(Click, cell[1].handle_collisions)

                if axis:
                    if self._switch:
                        self.visible_cells.append_column(cells)
                    else:
                        self.visible_cells.insert_column(-self._switch, cells)

                else:
                    if self._switch:
                        self.visible_cells.append_row(cells)
                    else:
                        self.visible_cells.insert_row(self._switch, cells)
                
                self._switch = not self._switch


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

        
        estimated_origin = list(position.get_index())

        estimated_origin[0] -=  (actual_length[0]-1)//2
        estimated_origin[1] -=  (actual_length[1]-1)//2

        origin = self.world_view.validate_origin(estimated_origin, actual_length)
        area_in_chunk = origin[0].verify_area(origin[1], actual_length)

        cells = self.world_view.get_cells(area_in_chunk)
        cells = self.world_view.complete_cells(cells, origin, actual_length)

        chunks = set([chunk[0] for chunk in cells])
        for chunk in chunks:
            self.world_view.render_adjacent_chunks(self, chunk)

        self.set_visible_chunks(chunks)
        self.set_visible_cells(cells)


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

