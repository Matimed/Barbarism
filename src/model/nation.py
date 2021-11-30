from src.model.charactors import Founder


class Nation:
    world = None

    @staticmethod
    def _get_world():
        return Nation.world

    def __init__(self):
        self.charactors = list()
        self.cities = []


    def add_charactor(self, position, charactor):
        self.charactors.append(charactor)
        Nation._get_world().add_entity(position, charactor)


    def get_charactor(self, index: int):
        return self.charactors[index]


    def get_next_charactor(self, charactor):
        try: 
            return self.charactors[self.charactors.index(charactor) + 1]
            
        except IndexError: raise StopIteration

    def has_charactor(self, charactor):
        """ Given a Position returns if there is a charactor
            of the Nation in that position.
        """

        return charactor in self.charactors