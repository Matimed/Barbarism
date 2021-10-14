from src.events import Event


class CellPressed(Event):
    def __init__(self, position):
        self.position = position

    
    def get_position(self):
        return self.position