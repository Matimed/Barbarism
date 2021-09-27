from events import Event


class EndScene(Event):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

    
    def get_scene(self): return self.scene