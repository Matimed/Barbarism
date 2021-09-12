from model import world
from view.scenes import Scene
from view.world_view import WorldView
from events import GlobalEvent as ev


class Game(Scene):
    def __init__(self):
        super().__init__()
        self.world = None

    
    def notify(self, events):
        for event in list(events):
            if event.type == ev.WORLD_GENERATED:
                self.world = WorldView(event.positions)

        if (self.world != None):
            self.world.draw(Scene.window_sur)
            Scene.window.update()
