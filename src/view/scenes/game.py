from src.events import Tick
from src.events import WorldGenerated
from src.view.scenes import Scene
from src.model.charactors import Founder


class Game(Scene):
    def __init__(self):
        super().__init__()
        self.world_view = None
        self.camera  = None

        ed = Scene.get_event_dispatcher()
        ed.add(WorldGenerated, self.generates_world_view)


    def generates_world_view(self, event):
        from src.view import WorldView
        from src.view import Camera

        world = event.get_world()

        self.world_view = WorldView(
            Scene.get_event_dispatcher(),
            world,
            Scene.get_window()
            )

        # Obtain the chunk and position where 
        # the game will start to be seen.
        spawn_point = world.generate_spawn_point()

        self.world_view.render_adjacent_chunks(
            Founder(),
            spawn_point[0]
            )

        self.camera = Camera(
            Scene.ed,
            Scene.window,
            self.world_view
            )
        
        self.camera.point(spawn_point[0],spawn_point[1])