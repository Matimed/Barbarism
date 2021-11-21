from src.events import Event


class Click(Event):
    def __init__(self, pos, button):
        super().__init__()

        self.pos = pos
        self.button = button

    
    def get_pos(self): return self.pos


    def get_button(self): return self.button