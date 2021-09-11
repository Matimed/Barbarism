from events import GlobalEvent as ev
from model import Nation
from model import Landlord 

class Logic:
    def __init__(self):
        self.nations = self.generate_nations()
        self.turn = self.nations[0]


    def generate_nations(self):
        """ Generates the different nations 
            that will be used in the game.
        """
        # We hardcoded... this should have a larger list of Nation and 
        # a better way to assing a Landlord to each one.
        nations = [ 
            Nation(Landlord(input('Input landlord name: ')))
            ]
        
        return nations

    
    def notify(self, events):
        for event in list(events):
            if event.type == ev.GAME_START:
                pass