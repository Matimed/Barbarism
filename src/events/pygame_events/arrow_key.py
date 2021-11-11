from src.events import Event


class ArrowKey(Event):
    def __init__(self, x = 0, y = 0):
        super().__init__()

        self.x = x
        self.y = y

    
    def get_x(self): return self.x

    def get_y(self): return self.y