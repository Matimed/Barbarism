from view import Window


class Scene:
    window = Window()
    window_sur = window.get_surface()

    def __init__(self):
        self.name = ''

    
    def notify(self, events):
        """ Recives a list of events and decide 
            how to interpret each one
        """

        raise NotImplementedError()

    
    def draw(self):
        """ Draws all the sprites it contains"""

        raise NotImplementedError()