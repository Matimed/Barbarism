

class Charactor:
    """ Abstract class that represents a person 
        or any other entity acting in a game.
    """

    # The choose of the word "Charactor" instead of "Character" 
    # is intentional to avoid any ambiguity because the word
    # Character can also mean "a single letter".

    
    def __init__(self):
        self.path = []
        self.speed = 2


    def change_path(self, route):
        """ Receives a list of positions and adds them to his path
            to be able to go through them later.
        """

        raise NotImplementedError