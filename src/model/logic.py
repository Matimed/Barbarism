from model import Nation 

class Logic:
    def __init__(self):
        self.nations = self.generate_nations()
        self.turn = self.nations[0]


    def generate_nations(self):
        """ Generates the different nations 
            that will be used in the game.
        """

        nations = []
        
        # For now we hardcoded the nation.
        nations.append(Nation()) 
        return nations