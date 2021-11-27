from enum import auto
from enum import IntEnum

class Layer(IntEnum):
    """ A separator of sprites. 
        The order of the variables here is the same order in which 
        they will be drawn.
    """

    CELL = auto()
    CHARACTOR = auto()