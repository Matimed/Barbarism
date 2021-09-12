import pygame
from events import GlobalEvent as ev
from model import Nation
from model import Landlord
from model import World 


class Logic:
    def __init__(self):
        self.nations = self._generate_nations()
        self.turn = self.nations[0]
        self.world = None


    def notify(self, events):
        for event in list(events):
            if event.type == ev.GAME_START:
                world = World()
                self.world = world
                Nation.world = world
                world_generated = pygame.event.Event(ev.WORLD_GENERATED.val, positions = world.get_positions())
                pygame.event.post(world_generated)



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

    