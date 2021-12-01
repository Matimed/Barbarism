from src.events import Event


class WorldUpdated(Event):
    def __init__(self, positions: list):
        """ Recives the updated positions.
        """
        
        super().__init__()
        self.positions = positions

    
    def get_positions(self): return self.positions