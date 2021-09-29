from events import Event


class Quit(Event):
    def __init__(self):
        super().__init__()