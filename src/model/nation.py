class Nation:
    def __init__(self, landlord):
        self.landlord = landlord
        self.charactor_posiition = {}
        self.cities = []

    def has_character(self, position):
        """ Given a Position returns if there is a charactor
            of the Nation in that position.
        """


        raise NotImplementedError