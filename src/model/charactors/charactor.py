

class Charactor:
    def __init__(self):
        self.path = []
        self.speed = 2


    def change_path(self, route):
        """ Receives a list of positions and adds them to his path
            to be able to go through them later.
        """

        raise NotImplementedError