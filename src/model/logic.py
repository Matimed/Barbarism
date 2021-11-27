from lib.weak_bound_method import WeakBoundMethod as Wbm
from src.events import GameStart
from src.events import PointEntity
from src.events import ShiftEnded
from src.events import WorldGenerated
from src.model.charactors import Founder
from src.model import Landlord
from src.model import Nation
from src.model import World 


class Logic:
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.ed.add(GameStart, self.game_start)

        self.nations = list()
        self.shift = tuple() # (Nation, Charactor)
        self.world: World = None # Will be initialized in game_start.


    def game_start(self, event):
        self.nations = self._create_nations(2)
        self.world = self._create_world()
        Nation.world = self.world
        self._position_nations()
        self.next_shift(ShiftEnded())

        position = self.world.get_entity_position(self.shift[1])

        self.ed.post(WorldGenerated(self.world))
        self.ed.post(
            PointEntity(
                self.shift[1],
                position,
                self.world.get_position(position.get_index())[0]
                ))
        

    def _create_world(self):
        world = World()
        Nation.world = world
        return world


    def _create_nations(self, number):
        return [Nation() for i in range(number)]


    def _position_nations(self):
        [nation.add_charactor(
            self.world.get_random_point()[1], Founder(nation)
            ) for nation in self.nations]

    
    def next_shift(self, event):
        try: 
            try: 
                self.shift[1] = self.shift[0].get_next_charactor(self.shift[1])

            except StopIteration:
                self.shift[0] = self.nations[self.nations.index(self.shift[0]) + 1]

        except IndexError: 
            self.shift = (
                self.nations[0], 
                self.nations[0].get_charactor(0)
                )