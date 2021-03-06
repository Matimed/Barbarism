import itertools as it
from lib.abstract_data_types import Matrix
from src.events import ArrowKey
from src.events import Click
from src.events import Tick
from src.events import Wheel
from src.references import Layer
from src.view.sprites import CellSprite
from src.view.sprites.sprite import Sprite


class Camera:
    def __init__(self, event_dispatcher, window, world_view):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.draw)
        self.ed.add(ArrowKey, self.move)
        self.ed.add(Wheel, self.zoom)

        self.window = window
        
        self.world = world_view

        self.visible_positions = Matrix()
        self.visible_sprites = dict() # {Position: {Layer: Sprite}}

        self.origin = (0,0)

        self._switch = 0

        # Minimum harcoded size for the cells matrix. 
        self.min_length = (3,5)
        self.max_length = self._calculate_length(Sprite.get_min_size())


    def is_visible(self, position):
        """ Returns true if the position passed is being seen.
        """
        
        return position in self.visible_positions


    def draw(self, event):
        self.draw_cells()
        for layer in Layer:
            if layer != Layer.CELL:
                self.draw_on_all_cells(layer)


    def draw_cells(self):
        """ Loops through the CellSprites of visible_sprites and draw them. 
        """

        last_p = self.origin # Last point.

        for row in self.visible_positions.iter_rows():
            for pos in row:
                cell = self.visible_sprites[pos][Layer.CELL]

                # We know that we are breaking OOP paradim
                # when we access an argument directly but 
                # this is neccesary because pygame does not have 
                # a suitable method of accessing the rect attributes.
                cell.rect.topleft = last_p
                last_p = cell.rect.topright
                cell.draw(self.window.get_surface())
            
            last_p = self.visible_sprites[row[0]][Layer.CELL].rect.bottomleft


    def draw_on_all_cells(self, layer):
        """ Pass all the sprites in the layer passed by parameter
            to the draw_on_cell method.
        """

        [self.draw_on_cell(
            self.visible_sprites[position][layer],
            position
            ) for position in self.visible_sprites 
            if layer in self.visible_sprites[position]]


    def draw_on_cell(self, sprite, position):
        """ Draws a sprite on the center of the cell with the 
            position passed by parameter.
        """

        sprite.rect.center = self.visible_sprites[position][Layer.CELL].rect.center
        sprite.draw(self.window.get_surface())


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
        origin = self.world.validate_origin(estimated_origin, actual_length)[1]

        new_sprites, removed_sprites = self.world.replace_cells(
            self, self.visible_positions, origin
            )


        self.update_visible_sprites(new_sprites)

        self._change_sprite_events(self.ed.remove, 
            {pos: self.visible_sprites.pop(pos) for pos in removed_sprites}
        )
        self._change_sprite_events(self.ed.add, new_sprites)

        self.origin = self._get_new_origin()
        self.refresh_sprites()


    def zoom(self, event):
        """ Receive the Wheel event and create the illusion of getting
            closer to the map by changing the CellSprites size and quantity.
        """
        
        actual_size = Sprite.get_actual_size()
        new_size = (actual_size + (event.get_movement() * (actual_size //10)))
        
        if new_size > Sprite.get_min_size():
            desired_length = self._calculate_length(new_size)

                
            if (
                event.get_movement() == 1 and 
                desired_length[0] >= self.min_length[0] and
                desired_length[1] >= self.min_length[1]
                ):
                
                self.set_sprites_size(new_size)
                self.zoom_in(desired_length)

            elif (
                event.get_movement() == -1 and
                desired_length[0] <= self.max_length[0] and
                desired_length[1] <= self.max_length[1]
                ):
                
                self.set_sprites_size(new_size)
                self.zoom_out(desired_length)
            
            self.refresh_sprites()


    def set_sprites_size(self, size):
        Sprite.set_size(size)

        [[
            sprite.update_size() 
            for sprite in dictionary.values()
            ]for dictionary in self.visible_sprites.values()
        ]


    def zoom_in(self, desired_size):
        """ Deletes cells of the visible_sprites dictionary until the quatity
            of cells be equal to the desired size passed by argument.
            Also desubscribes the deleted cells from the Click event.
        """

        actual_size = self.visible_positions.length()
        
        for _ in it.repeat(None, (actual_size[0] - desired_size[0])):
            row = self.visible_positions.pop_row(-(self._switch))
            
            self._change_sprite_events(
                self.ed.remove,
                {pos: self.visible_sprites.pop(pos) for pos in row}
                )

            self._switch = not self._switch

        for _ in it.repeat(None, (actual_size[1] - desired_size[1])):
            column = self.visible_positions.pop_column(-self._switch)

            self._change_sprite_events(
                self.ed.remove,
                {pos: self.visible_sprites.pop(pos) for pos in column}
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
        origin = self.world.validate_origin(estimated_origin, desired_length)[1]

        sprites = self.world.complete_cells(
            self, self.visible_positions, origin, desired_length
            )

        self.update_visible_sprites(sprites)
        self._change_sprite_events(self.ed.add, sprites)

        self.origin = self._get_new_origin()

    
    def update_visible_sprites(self, sprites: dict):
        """ Receives: dict{Position: list[Sprite]}
        """

        [sprite.update_size() for layer in sprites.values() for sprite in layer.values()]
        self.visible_sprites |= sprites


    def refresh_sprites(self):
        """ Executes the refresh method of all sprites in the visible_sprites
            dictionary in order to change they size.
        """
        
        [[
            sprite.refresh() 
            for sprite in dictionary.values()
            ]for dictionary in self.visible_sprites.values()
        ]


    def point(self, position):

        """ Receives a Position and its Chunk and centers them on screen.
        """
        if self.visible_sprites:
            self._change_sprite_events(self.ed.remove, self.visible_sprites)
            self.visible_sprites = dict()

        if self.visible_positions: 
            self._change_sprite_events(self.ed.remove, self.visible_sprites)

        actual_length = self._calculate_length(Sprite.get_actual_size())
        
        estimated_origin = list(position.get_index())
        estimated_origin[0] -=  (actual_length[0]-1)//2
        estimated_origin[1] -=  (actual_length[1]-1)//2

        origin = self.world.validate_origin(estimated_origin, actual_length)
        self.visible_positions = origin[0].verify_area(origin[1], actual_length)
        self.world.render_chunks(self, [origin[0]])
        new_sprites = self.world.get_cells(self.visible_positions)
        
        sprites = self.world.complete_cells(
            self, self.visible_positions, origin[1], actual_length
            )

        new_sprites |= sprites
        self.update_visible_sprites(new_sprites)

        self._change_sprite_events(self.ed.add, new_sprites)
            
        self.origin = self._get_new_origin()

        self.refresh_sprites()


    def _change_sprite_events(self, dispatcher_method, sprites):
        """ It receives an event method from the EventDispatcher and 
            applies it to the entire set of given cells. 
        """

        for dictionary in sprites.values():
            for layer in dictionary:
                if layer == Layer.CELL:
                    dispatcher_method(Click, dictionary[layer].handle_collisions)
                    
            

    def _get_new_origin(self):
        """ Calculates and returns the point 
            from which the cells should be drawn,
            based on the resolution, the zoom and the matrix length.
        """

        resolution = self.window.get_resolution()
        cell_size = Sprite.get_actual_size()
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