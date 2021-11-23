from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from random import choice
from src.references import Biome


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """

    def __init__(self, order = 1000):
        self.order = order
        self.positions: Matrix = self._generate_positions(order)
        self.chunks: Matrix = self._generate_chunks(25, order, self.positions)
        self.cells: dict = self._generate_cells(self.positions)


    def get_position(self, position_index) -> (Chunk,Position):
        """ Returns the chunk and position 
            object that match with the given position index.
        """
        
        position = self.positions.get_element(position_index)
        length = Chunk.get_length()

        chunk_index = (
            position_index[0] // (length[0]), position_index[1] // (length[1])
        )

        chunk = self.chunks.get_element(chunk_index)

        if not chunk.has(position): raise KeyError()

        return (chunk, position)


    def get_adjacent_chunks(self, chunk) -> list:
        """ Returns the list of Chunk objects 
            adjacent to the one given by parameter.
        """

        return self.chunks.get_adjacencies(self.chunks.index(chunk))


    def get_adjacent_positions(self, position) -> list:
        """ Returns the list of Position objects 
            adjacent to the one given by parameter.
        """

        return self.positions.get_adjacencies(self.positions.index(position))


    def create_route(self, origin, destination):
        """ Given two Position returns the fastest way
            to get from the origin to the destination point.
        """

        raise NotImplementedError


    def get_limit(self) -> Position:
        """ Returns the last Position in the world.
        """

        index = self.positions.get_last_index()
        return self.positions.get_element(index)


    def _generate_positions(self, order):
        """ Generates a Matrix of Position type objects 
            based on the given size (order).
        """

        return Matrix(Position.create_collection((0,0), (order -1 ,order -1)))


    def _generate_chunks(self, min_size:int, order, positions):
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        size = min_size
        while True:
            if not (order%size):
                break
            size +=1

        splited_positions = positions.split(order/size)

        return Matrix([[Chunk(positions, (y,x)) for x, positions in enumerate(row)]
            for y, row in enumerate(splited_positions.iter_rows())])


    def _generate_cells(self, positions:iter) -> dict:
        """ Receives an iterable of Position type objects and
            generate a dict of Biomes with a position as key.
        """
        
            
        return {position:Biome.GRASS for row in positions.iter_rows()
            for position in row}


    def generate_spawn_point(self) -> (Chunk, Position):
        """ Returns a Chunk and a Position on that 
            chunk where to place a charactor.
        """

        # In the future a more complex spawn method will be implemented.
        chunk = self.chunks.random()
        return (chunk, chunk.get_random_position())

    
    def get_cells(self, positions:iter):
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """

        return {position:self.cells[position] for position in positions}
        
        