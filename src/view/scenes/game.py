from src.events import Tick
from src.events import WorldGenerated
from src.view.scenes import Scene


class Game(Scene):
    def __init__(self):
        super().__init__()
        self.world_view = None
        ed = Scene.get_event_dispatcher()
        ed.add(Tick,self.update)
        ed.add(WorldGenerated, self.generates_world_view)


    def generates_world_view(self, event):
        from src.view import WorldView
        
        self.world_view = WorldView(
            self.get_event_dispatcher(),
            event.get_world(),
            Scene().get_window()
            )


    def update(self, event):
        if (self.world_view != None):
            self.world_view.draw(Scene.get_window_sur())
            Scene.get_window().update()