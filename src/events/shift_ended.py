from src.events import Event


class ShiftEnded(Event):
    def __init__(self):
        super().__init__()