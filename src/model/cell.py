from recordclass import dataobject

class Cell(dataobject, fast_new = True):
    """ A minimum unity of land that shapes the World.
    """

    __fields__ = ['friction']
