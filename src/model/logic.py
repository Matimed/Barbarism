from src.events import CellPressed
from src.events import GameStart
from src.events import PointEntity
from src.events import ShiftEnded
from src.events import WorldGenerated
from src.model.biomes_manager import BiomesManager
from src.model.charactors import Charactor
from src.model.charactors import Founder
from src.model.charactors import Warrior
from src.model import Nation
from src.model import World 


class Logic:
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher

        Charactor.set_event_dispatcher(self.ed)
        
        self.ed.add(GameStart, self.game_start)
        self.ed.add(CellPressed, self.cell_interaction)
        self.ed.add(ShiftEnded, self.next_shift)


        self.nations = list()
        self.shift = list() # (Nation, Charactor)
        self.world: World = None # Will be initialized in game_start.


    def game_start(self, event):
        self.nations = self._create_nations(2)
        self.world = self._create_world()
        Nation.world = self.world
        self._position_nations()
        self.shift = [
                self.nations[0],
                self.nations[0].get_charactor(0)
            ]

        self.ed.post(WorldGenerated(self.world))
        self.point_current_charactor()
        

    def _create_world(self):
        world = World(self.ed)
        Nation.world = world
        return world


    def _create_nations(self, number):
        return [Nation() for i in range(number)]


    def _position_nations(self):
        for nation in self.nations:
            positions = iter(self.world.generate_spawn_points(quantity=2))
            nation.add_charactor(next(positions), Founder(nation))
            nation.add_charactor(next(positions), Warrior(nation))

    
    def next_shift(self, event):
        """ Updates the shift.
        """

        if len(self.shift) == 2: 
            if self.shift[1].has_path():
                self.update_charactor_path(self.shift[1].get_destination())
                self.shift[1].move()

        # Will fail if it's the last shift.
        try: 
            # Will fail if it's the last charactor of the nation.
            try:
                self.shift[1] = self.shift[0].get_next_charactor(self.shift[1])
                self.point_current_charactor()

            except StopIteration:
                self.shift[0] = self.nations[self.nations.index(self.shift[0]) + 1]
                self.shift[1] = self.shift[0].get_charactor(0)
                self.point_current_charactor()

        except IndexError:
            self.shift = [
                self.nations[0],
                self.nations[0].get_charactor(0)
            ]
            self.point_current_charactor()


    def point_current_charactor(self):
        position = self.world.get_entity_position(self.shift[1])
        self.ed.post(PointEntity(
            self.shift[1],
            position,
            self.world.get_position(position.get_index())[0]
        ))


    def cell_interaction(self, event):
        cell = self.world.get_cells([event.get_position()])

        if BiomesManager.get_passable(cell[event.get_position()]):
            self.update_charactor_path(event.get_position())


    def update_charactor_path(self, destination):
        origin = self.world.get_entity_position(self.shift[1])
        path = self.world.create_route(origin, destination)
        self.shift[1].set_path(path)