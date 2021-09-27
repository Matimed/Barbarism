from weak_bound_method import WeakBoundMethod as Wbm
from view.scenes import Scene
from view.world_view import WorldView
from events import WorldGenerated
from events import Tick


class Game(Scene):
    def __init__(self):
        super().__init__()
        self.world = None
        ed = Scene.get_event_dispatcher()
        ed.add(Tick, Wbm(self.update))
        ed.add(WorldGenerated, Wbm(self.generates_world_view))


    def generates_world_view(self, event):
        self.world = WorldView(
            self.get_event_dispatcher(),
            event.get_positions()
            )


    def update(self, event):
        if (self.world != None):
            self.world.draw(Scene.get_window_sur())
            Scene.get_window().update()