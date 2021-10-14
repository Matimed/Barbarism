from src.view.scenes import Scene
from src.view.scenes import MainMenu
from src.view.scenes import Game
from src.events import EndScene
from src.events import BackMenu
from src.events import GameStart


class SceneManager:
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        Scene.ed = self.ed

        self.ed.add(BackMenu, self.back_menu)
        self.ed.add(EndScene, self.end_scene)

        self.scenes = {
            'menu' : MainMenu,
            'game' : Game
        }
        self.current_scene = None

        self._set_current_scene(self.scenes['menu'])

    
    def back_menu(self, event):
        self._set_current_scene(self.scenes['menu'])


    def end_scene(self, event):
        scene = event.get_scene()

        if scene == self.scenes['menu']:
            self._set_current_scene(self.scenes['game'])
            self.ed.post(GameStart())


    def _set_current_scene(self, scene):
        """ Change the current scene for another
        
            Receives:
                scene:<scene>
        """

        self.current_scene = scene()

