from src.events import Event


class MoveEntity(Event):
    def __init__(self, entity, destination):
        """ Recives the entity and the postion to move it.
        """

        super().__init__()
        self.entity = entity
        self.destination = destination

    
    def get_destination(self): return self.destination


    def get_entity(self): return self.entity