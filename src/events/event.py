

class Event:
    """ Information used by the EventDispatcher to notify 
        an object to perform a certain action.
        It can contain attributes to perform this action.
    """

    @classmethod
    def get_class(cls):
        return cls