from src.events import Event


class WorldGenerated(Event):
    def __init__(self, world):
        self.world = world


    def get_world(self):
        return self.world