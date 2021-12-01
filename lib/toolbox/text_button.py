import pygame as pg
from lib.toolbox import TextBox


class TextButton(pg.sprite.Sprite):
    """ An interactive button that adjusts its length according to the text it contains.
        It has two states that are: pressed and released (not released).
        The only thing that changes between these two states is the right part of the button.
    """

    def __init__(self, images:dict, font, click_event, event_dispatcher, 
            text, height, color=(0,0,0), sound=None):
        """ Images must contain the following keys:
            'left', 'middle', 'right' and 'right_pressed'.
        """

        super().__init__()
        self.images = images
        self.text = TextBox(font, text, color)
        self.height = height
        self.sound = sound
        
        self.native_size = self._get_native_size() # Unscaled button size. 
        self.button = self._image_creator()
        self.image = self.button[0]
        self.rect = self.image.get_rect()
        
        event_dispatcher.add(click_event, handle_collisions)
    
    
    def draw(self, surface:pg.Surface):
        """ It receives a surface and draws itself on it.
        """

        surface.blit(self.image, self.rect)


    def get_rect(self):
        return self.rect


    def handle_collisions(self, event):
        """ It is called every time the click event is triggered
            and returns True if the button was pressed.
        """

        return self.rect.collidepoint(event.get_pos()) \
            and event.get_button() == 1

            

    def _get_native_size(self):
        """ Gets the size of the button based on its text attribute.
        """

        height = self.images['left'].get_size()[1]
        
        width = self.images['left'].get_size()[0]
        width += self.images['middle'].get_size()[0] * (self.text.get_size()[0] - 1)
        width += self.images['right'].get_size()[0]        

        return [width, height]


    def _image_creator(self):
        """ Create the surfaces of the pressed button and 
            the button released.
        """

        surface = [] 
        surface.append(pg.Surface(self.native_size, pg.SRCALPHA))

        self._draw_left_part(surface[0])
        self._draw_middle_part(surface[0])
        self._draw_text(surface[0])

        surface.append(surface[0].copy()) 

        self._draw_right_part(surface[0])
        self._draw_right_part(surface[1], True)

        for i in range(len(surface)):
            surface[i] = self._scale(surface[i], self.height)

        return surface


    def _draw_left_part(self, surface):
        """ On the surface received by argument draw
            the left part that will have the button.
        """

        surface.blit(self.images['left'], (0, 0))


    def _draw_middle_part(self, surface):
        """ On the surface received by argument draw
            the central part that will have the button.
        """

        for i in range(
                self.images['left'].get_size()[0], 
                self.native_size[0] - self.images['right'].get_size()[0], 
                self.images['middle'].get_size()[0]):
            
            surface.blit(self.images['middle'], (i, 0))

        
    def _draw_right_part(self, surface, pressed=False):
        """ Depending on your argument 'pressed' draws on the surface 
            passed by argument the right part which will have the button.
        """

        part = None
        
        if pressed: part = self.images['right_press']
        else: part = self.images['right'] 
            
        surface.blit(part,(self.native_size[0] - part.get_size()[0], 0))
        

    def _draw_text(self, surface):
        """ On the surface received by argument draw
            the text that the button will have.
        """

        self.text.get_rect().midleft = (
            self.images['left'].get_size()[0], 
            ((self.images['middle'].get_size()[1] / 2))
        )
        
        surface.blit(self.text.get_surface(), self.text.get_rect())    


    def _scale(self, surface, height):
        """ Scale a surface to a certain height.
        """
        
        native_length = surface.get_size()[0]
        native_height = surface.get_size()[1]

        scale = height // native_height

        return pg.transform.scale(
            surface, (native_length * scale, native_height  * scale)
        )
