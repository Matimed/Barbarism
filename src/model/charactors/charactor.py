from src.events import MoveEntity
from src.model import Entity


class Charactor(Entity):
    """ Abstract class that represents a person 
        or any other entity acting in a game.
    """

    ed = None # EventDispatcher

    # The choose of the word "Charactor" instead of "Character" 
    # is intentional to avoid any ambiguity because the word
    # Character can also mean "a single letter".

    @classmethod
    def set_event_dispatcher(cls, ed, avoidable=True):
        cls.ed = ed


    def __init__(self, nation):
        self.nation = nation
        self.path = list()
        self.speed = 2

    def has_path(self): return bool(self.path)


    def get_nation(self): return self.nation


    def get_destination(self): return self.path[0]


    def set_path(self, path):
        """ Receives a list of positions and adds them to his path
            to be able to go through them later.
        """
        
        self.path = path

    
    def move(self):
        
        if self.path:
            position = self.path.pop()

            self.ed.post(MoveEntity(self, position))