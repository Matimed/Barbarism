from lib.weak_bound_method import WeakBoundMethod as Wbm
from src.events import GameStart
from src.events import WorldGenerated
from src.model import Landlord
from src.model import Nation
from src.model import World 


class Logic:
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.ed.add(GameStart, self.game_start)

        self.nations = self._generate_nations()
        self.turn = self.nations[0]
        self.world = None

    def game_start(self, event):
        world = World()
        self.world = world
        Nation.world = world
        self.ed.post(WorldGenerated(world))


    def _generate_nations(self):
        """ Generates the different nations 
            that will be used in the game.
        """
        # We hardcoded... this should have a larger list of Nation and 
        # a better way to assing a Landlord to each one.
        nations = [ 
            Nation(Landlord('Player'))
            ]
        
        return nations

    