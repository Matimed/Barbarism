from model import Nation
from model import Landlord
from model import World 
from events import GameStart
from events import WorldGenerated
from weak_bound_method import WeakBoundMethod as Wbm


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
        self.ed.post(WorldGenerated(world.get_positions()))


    def _generate_nations(self):
        """ Generates the different nations 
            that will be used in the game.
        """
        # We hardcoded... this should have a larger list of Nation and 
        # a better way to assing a Landlord to each one.
        nations = [ 
            Nation(Landlord(input('Input landlord name: ')))
            ]
        
        return nations

    