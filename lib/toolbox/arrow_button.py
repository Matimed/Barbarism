import pygame as pg


class ArrowButton(pg.sprite.Sprite):
    """ An interactive arrow-shaped button
        whose angle can be modified
    """

    def __init__(self, pressed_image, unpressed_image, 
            click_event, event_dispatcher, height, angle=0, sound=None):

        super().__init__()
        self.ed = event_dispatcher
        self.images = images
        self.button = [
            self._adjust_surface(pressed_image, height, angle),
            self._adjust_surface(unpressed_image, height, angle)
        ]
        

        self.index = 0
        self.image = self.button[self.index]

        self.rect = self.image.get_rect()
        self.sound = sound

        event_dispatcher.add(click_event, self.handle_collisions)


    def handle_collisions(self, event):
        """ It is called every time the click event is triggered
            and returns True if the button was pressed.
        """

        return self.rect.collidepoint(event.get_pos()) and \
            event.get_button() == 1


    def _adjust_surface(self, surface, height, angle):
        """ Apply a certain scale and tilt
            according to the arguments received
        """

        surface = self._scale(surface, height)
        surface = pg.transform.rotozoom(surface, angle, 1)

        return surface


    def get_rect(self): return self.rect


    def get_surface(self): return self.image

    
    def draw(self, surface):
        """ Recives a surface and draws itself on it
        """

        surface.blit(self.image, self.rect)


    def _scale(self, surface, height):
        """ Scales a surface to a certain height
        """

        native_lenght = surface.get_size()[0]
        native_height = surface.get_size()[1]

        scale = height//native_height

        return pg.transform.scale(
            surface, (native_lenght*scale, native_height*scale)
        )
