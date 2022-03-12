from src.events import Tick
from src.events import PointEntity
from src.events import WorldUpdated
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
        ed.add(WorldUpdated, self.update_sprites)


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
        chunks = self.world_view.get_adjacent_chunks([event.get_chunk()])
        self.world_view.set_renderized_chunks(event.get_entity(), chunks)
        
        self.camera.point(event.get_position())

    
    def update_sprites(self, event):
        """ Updates the state of the sprites 
            in the world_view and the camera.
        """
        
        self.world_view.update_entities(event.get_positions())

        for position in event.get_positions():
            # If the position is not being renderized 
            # world_view will not care about update sprites.
            if self.world_view.is_renderized(position):
                sprites = self.world_view.get_sprites([position])

                # If the position is not being seen 
                # camera will not care about update sprites.
                if self.camera.is_visible(position):
                    self.camera.update_visible_sprites({position: sprites[position]})