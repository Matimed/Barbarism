from events import Event


class Tick(Event):
    instances = {}

    def __init__(self):
        super().__init__()


    def __new__(cls):
        """ Implements singleton pattern to prevent
            more than one instantiation.
        """

        if cls not in cls.instances:
            instance = super().__new__(cls)
            cls.instances[cls] = instance

        return cls.instances[cls]