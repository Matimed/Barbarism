from src.model.charactors import Aggressive


class Warrior(Aggressive):
    """ An aggressive character that is able to fight.
    """
    
    def __init__(self, nation):
        super().__init__(nation)

    