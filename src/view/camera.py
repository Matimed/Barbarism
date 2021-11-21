from src.view.sprites import CellSprite
from src.events import Tick
from src.events import Wheel
from src.events import ArrowKey
from lib.abstract_data_types import Matrix
from src.events import Click
import itertools as it


class Camera:
    def __init__(self, event_dispatcher, window, world_view):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.draw)
        self.ed.add(ArrowKey, self.move)
        self.ed.add(Wheel, self.zoom)

        self.window = window

        self.world = world_view

        self.visible_positions = Matrix()
        self.visible_sprites = dict() # {Position: list[Sprite]}

        self.origin = (0,0)

        self._switch = 0

        # Minimum harcoded size for the cells matrix. 
        self.min_length = (3,5)
        self.max_length = self._calculate_length(CellSprite.get_min_size())


    def draw(self, event):
        """ Loops through the CellSprites of visible_sprites and draw them. 
        """

        previous_point = self.origin

        for row in self.visible_positions.iter_rows():
            for pos in row:
                cell = self.visible_sprites[pos][0]

                # We know that we are breaking OOP paradim
                # when we access an argument directly but 
                # this is neccesary because pygame does not have 
                # a suitable method of accessing the rect attributes.
                cell.rect.topleft = previous_point
                previous_point = cell.rect.topright
                cell.draw(self.window.get_surface())
            
            previous_point = self.visible_sprites[row[0]][0].rect.bottomleft


    def move(self, event):
        """ Receive the ArrowKey event and according to the arrow direction
            adds a row/column at the end and remove another at the beginning
            to give the sensation of movement.
        """

        first_pos = self.visible_positions.get_element((0,0))
        estimated_origin = list(first_pos.get_index())

        estimated_origin[0] -= event.get_y()
        estimated_origin[1] += event.get_x()
                        
        actual_length = self.visible_positions.length()
        origin = self.world.validate_origin(estimated_origin, actual_length)

        new_sprites, removed_sprites = self.world.replace_cells(
            self, self.visible_positions, origin
            )

        self.visible_sprites |= new_sprites

        self._change_cell_events(
            self.ed.remove,
            [sprite[0] for sprite in removed_sprites.values()]
            )

        self._change_cell_events(
            self.ed.add,
            [sprite[0] for sprite in new_sprites.values()]
            )

        self.origin = self._get_new_origin()
        self.refresh_sprites()


    def zoom(self, event):
        """ Receive the Wheel event and create the illusion of getting
            closer to the map by changing the CellSprites size and quantity.
        """
        
        actual_size = CellSprite.get_actual_size()
        new_size = (actual_size + (event.get_movement() * (actual_size //10)))
        
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
            
            self.refresh_sprites()


    def zoom_in(self, desired_size):
        """ Deletes cells of the visible_sprites dictionary until the quatity
            of cells be equal to the desired size passed by argument.
            Also desubscribes the deleted cells from the Click event.
        """

        actual_size = self.visible_positions.length()
        
        for _ in it.repeat(None, (actual_size[0] - desired_size[0])):
            row = self.visible_positions.pop_row(-(self._switch))
            
            self._change_cell_events(
                self.ed.remove,
                [self.visible_sprites[pos][0] for pos in row]
                )

            self._switch = not self._switch

        for _ in it.repeat(None, (actual_size[1] - desired_size[1])):
            column = self.visible_positions.pop_column(-self._switch)

            self._change_cell_events(
                self.ed.remove,
                [self.visible_sprites[pos][0] for pos in column]
                )

            self._switch = not self._switch
        
        self.origin = self._get_new_origin()
        

    def zoom_out(self, desired_length):
        """ Adds cells of the visible_sprites dictionary  until the quatity
            of cells be equal to the desired size passed by argument.
            Also subscribes the cells to the Click event.
        """

        actual_length = self.visible_positions.length()
        
        first_pos = self.visible_positions.get_element((0,0))
        estimated_origin = list(first_pos.get_index())

        if self._switch and actual_length != desired_length:            

            if actual_length[0] < desired_length[0]: estimated_origin[0] -= 1
            if actual_length[1] < desired_length[1]: estimated_origin[1] -= 1

            self._switch = not self._switch
                        
        origin = self.world.validate_origin(
            estimated_origin, desired_length
        )
        
        cells = self.get_visible_cells()

        sprites = self.world.complete_cells(
            self, self.visible_positions, origin, desired_length
            )

        self.update_visible_sprites(sprites)

        self._change_cell_events(
            self.ed.add,
            [sprite[0] for sprite in sprites.values()]
            )

        self.origin = self._get_new_origin()


    def get_visible_cells(self):
        return [self.visible_sprites[pos][0] for pos in self.visible_sprites]

    
    def update_visible_sprites(self, sprites: dict):
        """ Receives: dict{Position: list[Sprite]}
        """

        self.visible_sprites |= sprites


    def refresh_sprites(self):
        """ Executes the refresh method of all sprites in the visible_sprites
            dictionary in order to change they size.
        """
        
        [[
            sprite.refresh() 
            for sprite in self.visible_sprites[pos]
            ]for pos in self.visible_sprites
        ]


    def point(self, chunk, position):

        """ Receives a Position and its Chunk and centers them on screen.
        """

        if self.visible_positions: 
            self._change_cell_events(self.ed.remove, self.get_visible_cells())

        actual_length = self._calculate_length(CellSprite.get_actual_size())
        
        estimated_origin = list(position.get_index())
        estimated_origin[0] -=  (actual_length[0]-1)//2
        estimated_origin[1] -=  (actual_length[1]-1)//2

        origin = self.world.validate_origin(estimated_origin, actual_length)
        self.visible_positions = origin[0].verify_area(origin[1], actual_length)

        new_sprites = self.world.get_cells(self.visible_positions)
        
        sprites = self.world.complete_cells(
            self, self.visible_positions, origin, actual_length
            )

        new_sprites |= sprites
        self.visible_sprites |= new_sprites

        self._change_cell_events(
            self.ed.add, [sprite[0] for sprite in new_sprites.values()]
            )
            
        self.origin = self._get_new_origin()


    def _change_cell_events(self, method, cells):
        """ It receives an event method from the EventDispatcher and 
            applies it to the entire set of given cells. 
        """

        for cell in cells:
            method(Click, cell.handle_collisions)


    def _get_new_origin(self):
        """ Calculates and returns the point 
            from which the cells should be drawn,
            based on the resolution, the zoom and the matrix length.
        """

        resolution = self.window.get_resolution()
        cell_size = CellSprite.get_actual_size()
        length = self.visible_positions.length()

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

