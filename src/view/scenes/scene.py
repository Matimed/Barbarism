from src.view import Window


class Scene:
    window = Window()
    window_sur = window.get_surface()
    ed = None # EventDispatcher
    
    @staticmethod
    def set_event_dispatcher(event_dispatcher):
        Scene.ed = event_dispatcher


    @staticmethod
    def get_event_dispatcher():
        return Scene.ed


    @staticmethod
    def get_window():
        return Scene.window


    @classmethod
    def get_window_sur(cls):
        return Scene.window_sur


    def __init__(self):
        self.name = ''

    
    def update(self, event):
        """ Updates all the sprites it contains"""

        raise NotImplementedError()

    
    def draw(self):
        """ Draws all the sprites it contains"""

        raise NotImplementedError()