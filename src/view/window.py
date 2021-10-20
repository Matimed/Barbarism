import pygame


class Window:
    """ Implements all that concerns to the pygame class diplay
        and a backgroun managment
    """

    def __init__(self):
        pygame.display.set_caption('Barbarisim')
        
        self.max_resolution = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h
        ) # Obtains the resolution of the screen.
        

        # Minimum resolution by default.
        self.native_resolution = (480, 270)

        self.scale = 2 # Default scale.

        # Current resolution.
        self.resolution = self.create_resolution(self.scale)

        self.window_sur = pygame.display.set_mode(self.resolution)


        self.background = None
        self.set_background((0,0,0))

    
    def get_surface(self):
        """ Obtains the display surface.
        """
        
        return self.window_sur

    
    def update(self):
        """ Update the display and draw the background.
        """

        pygame.display.update()
        self.window_sur.blit(self.background, (0,0))


    def create_resolution(self, scale):
        """ Recives:
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
            
            Recives:
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

        self.window_sur = pygame.display.set_mode(self.resolution, flags)

        self._reset_background() # The background must adapt to the new resolution.


    def get_resolution(self) -> tuple[int,int]:
        """ Returns the current resolution.
        """

        return self.resolution


    def set_background(self, color=(0,0,0)):
        """ Change the color of the display background.
            
            Recives:
                color:<tuple>
        """

        background_sur = pygame.Surface(self.resolution)
        background_sur.fill(color)
        
        self.background = background_sur


    def _reset_background(self):
        """ Scale the background according to the screen resolution.
        """

        self.background = pygame.transform.scale(self.background, (self.resolution))