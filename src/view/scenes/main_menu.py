from events import Tick
from view.scenes import Scene
from events import EndScene


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Scene.get_event_dispatcher().add(Tick, self.update)


    def update(self, event):
        # For now this event will be here to speed up the start of the game. 
        Scene.get_event_dispatcher().post(EndScene(self.__class__))