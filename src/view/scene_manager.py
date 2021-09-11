from view.scenes import MainMenu
from view.scenes import Game
from events import GlobalEvent as ev


class SceneManager:
    def __init__(self):
        self.scenes = {
            'menu' : MainMenu,
            'game' : Game
        }
    
        self.current_scene = self.scenes['menu']()


    def notify(self, events):
        for event in list(events):
            if event.type == ev.BACK_MENU:
                self._set_current_scene(self.scenes['menu'])
                events.remove(event) # The scenes don't need this events.

            if event.type == ev.END_SCENE:
                if event.scene == self.scenes['menu']:
                    self._set_current_scene(self.scenes['game'])

                events.remove(event)

        self.current_scene.notify(events)


    def _set_current_scene(self, scene):
        """ Change the current scene for another
        
            Receives:
                scene:<scene>
        """

        self.current_scene = scene()

