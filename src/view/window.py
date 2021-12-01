import pygame as pg


class Window:
    """ Implements all that concerns to the pygame class diplay
        and a backgroun managment
    """

    def __init__(self):
        pg.display.set_caption('Barbarism')
        pg.display.set_icon(pg.image.load('assets/graphics/icon.png'))

        self.max_resolution = (
            pg.display.Info().current_w,
            pg.display.Info().current_h
        ) # Obtains the resolution of the screen.
        

        # Minimum resolution by default.
        self.native_resolution = (480, 270)

        self.scale = 2 # Default scale.

        # Current resolution.
        self.resolution = self.create_resolution(self.scale)

        self.window_sur = pg.display.set_mode(self.resolution)


        self.background = None
        self.set_background((0,0,0))

    
    def get_surface(self):
        """ Obtains the display surface.
        """
        
        return self.window_sur

    
    def update(self, event):
        """ Update the display and draw the background.
        """

        pg.display.update()
        self.window_sur.blit(self.background, (0,0))


    def create_resolution(self, scale):
        """ Receives:
                scale:<int>
            Returns:
                resolution:<tuple> scaled native resolution.
        """

        resolution = [
            int(self.native_resolution[0] * scale), 
            int(self.native_resolution[1] * scale)
            ]
        
        return resolution

    
    def fit_screen(self, scale, flags = 0):
        """ Change the display size to other scale.
            
            Receives:
                scale:<int> new scale
                flags:<int> pygame enum.
        """

        assert (
            self.create_resolution(scale)[0] > self.max_resolution[0]
            or self.create_resolution(scale)[1] > self.max_resolution[1]), (
            'The resolution that is obtained with that scale is too large.'
        )
        assert scale >= 1,(
            'The resolution that is obtained with that scale is too small.'
            )

        self.scale = scale
        self.resolution = self.create_resolution(scale)

        self.window_sur = pg.display.set_mode(self.resolution, flags)

        self._reset_background() # The background must adapt to the new resolution.


    def get_resolution(self) -> tuple[int,int]:
        """ Returns the current resolution.
        """

        return self.resolution


    def set_background(self, color=(0,0,0)):
        """ Change the color of the display background.
            
            Receives:
                color:<tuple>
        """

        background_sur = pg.Surface(self.resolution)
        background_sur.fill(color)
        
        self.background = background_sur


    def _reset_background(self):
        """ Scale the background according to the screen resolution.
        """

        self.background = pg.transform.scale(self.background, (self.resolution))