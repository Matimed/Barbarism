from src.model.charactors import Charactor


class Passive(Charactor):
    """ Any person or entity that can not fight.
    """

    def __init__(self, nation):
        super().__init__(nation)