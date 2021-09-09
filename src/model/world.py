

class World:
    def __init__(self):
        self.cells = {}


    def create_route(self, origin, destination):
        """ Given two Position returns the fastest way
            to get from the origin to the destination point.
        """

        raise NotImplementedError