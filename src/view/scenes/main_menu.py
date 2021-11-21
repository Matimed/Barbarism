from src.events import EndScene
from src.events import Tick
from src.view.scenes import Scene


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Scene.get_event_dispatcher().add(Tick, self.update)


    def update(self, event):
        # For now this event will be here to speed up the start of the game. 
        Scene.get_event_dispatcher().post(EndScene(self.__class__))