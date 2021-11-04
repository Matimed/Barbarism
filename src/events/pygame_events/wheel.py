from src.events import Event


class Wheel(Event):
    def __init__(self, movement):
        super().__init__()

        self.movement = movement

    
    def get_movement(self): return self.movement