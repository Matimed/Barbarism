from src.events import Event


class WorldGenerated(Event):
    def __init__(self, positions):
        self.positions = positions

    
    def get_positions(self):
        return self.positions