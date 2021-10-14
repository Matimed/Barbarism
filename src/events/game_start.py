from src.events import Event


class GameStart(Event):
    def __init__(self):
        super().__init__()