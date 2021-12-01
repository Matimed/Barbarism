import pygame as pg


class TextBox(pg.sprite.Sprite):
    """ Class to represent a text on the screen.
    """

    def __init__(self, font, text, color=(0,0,0), height=8, long_spaces=True):
        super().__init__()
        self.color = color
        self.height = height
        self.font = font

        # Variable used for fonts with very short spaces to lengthen them.
        self.long_spaces = long_spaces

        self.rect = None
        self.image = None

        self.set_text(text) 
        self.text = self.get_text()
        
        
    def draw(self, surface):
        """ It receives a surface and draws itself on it.
        """

        surface.blit(self.image, self.rect)


    def get_rect(self): return self.rect


    def get_surface(self): return self.image


    def get_size(self): return self.image.get_size() 


    def set_text(self, text):

        if text == '': text = ' '
        self.text = text

        if self.long_spaces:
            text = text.replace(" ", "    ")
        
        self.image = self._scale(
            self.font.render(text, True, self.color), self.height
            )
        
        if self.rect: location = self.rect.center
        else: location = (0,0)
        
        self.rect = self.image.get_rect()
        self.rect.center = location

    
    def get_text(self):
        text = self.text
        if text == ' ': text = ''
        return text

    
    def _scale(self, surface, height):
        """ Scales the surface to a certain height.
        """

        native_width = surface.get_size()[0]
        native_height = surface.get_size()[1]

        scale = height // native_height

        return pg.transform.scale(
            surface, (native_width * scale, native_height  * scale)
        )