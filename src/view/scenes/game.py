from src.events import Tick
from src.events import PointEntity
from src.events import WorldGenerated
from src.model.charactors import Founder
from src.view.scenes import Scene
from src.references import Layer


class Game(Scene):
    def __init__(self):
        super().__init__()
        self.world_view = None
        self.camera  = None

        ed = Scene.get_event_dispatcher()
        ed.add(WorldGenerated, self.create_view_objects)
        ed.add(PointEntity, self.point_entity)
        ed.add(Tick, Scene.window.update)


    def create_view_objects(self, event):
        from src.view import WorldView
        from src.view import Camera

        world = event.get_world()

        self.world_view = WorldView(
            Scene.get_event_dispatcher(),
            world,
            Scene.get_window()
            )

        self.camera = Camera(
            Scene.ed,
            Scene.window,
            self.world_view
            )


    def point_entity(self, event):
        self.world_view.render_adjacent_chunks(
            event.get_entity(),
            set([event.get_chunk()])
            )
        
        self.camera.point(event.get_position())