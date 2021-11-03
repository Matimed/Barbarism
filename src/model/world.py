from src.model.cells import Plain
from lib.position import Position
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from random import choice


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """

    def __init__(self, order = 100):
        self.order = order
        self.positions: Matrix = self._generate_positions(order)
        self.cells: dict = self._generate_cells(self.positions)
        self.chunks: Matrix = self._generate_chunks(10)


    def get_position(self, position_index):
        position = self.positions.get_element(position_index)

        for chunk in self.chunks:
            if chunk.has(position): break

        return (chunk, position)


    def get_position_by_chunk(self, position_index, chunk_index):
        """ Returns the fragment and position 
            object that match the given indices.
        """
        
        position = self.positions.get_element(position_index)
        chunk = self.chunks.get_element(chunk_index)
        
        if chunk.has(position):
            return (chunk, position)
        
        else: return False


    def get_biomes(self):
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """
        
        raise NotImplementedError


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

        positions = Matrix()

        for y in range(order):
            row_positions = []
            
            for x in range(order):
                row_positions.append(Position(y, x))
            
            positions.append_row(row_positions)

        return positions


    def _generate_chunks(self, min_size:int):
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        size = min_size
        while True:
            if not (self.order%size):
                break
            size +=1

        splited_positions = self.positions.split(self.order/size)
        chunks = Matrix()

        for y, row in enumerate(splited_positions.iter_rows()):
            chunk_row = []
            for x, position in enumerate(row):
                chunk= Chunk(position,(y,x))
                chunk_row.append(chunk)

            chunks.append_row(chunk_row)

        return chunks


    def _generate_cells(self, positions):
        """ Recives a Matrix of Position type objects and
            generate a dict of Cell type objects with a position as key.
        """
        
        cells = {}

        for i in positions:
            cells[i] = Plain()

        return cells


    def generate_spawn_point(self) -> tuple[Chunk, Position]:
        """ Returns a Chunk and a Position on that 
            chunk where to place a charactor.
        """

        # In the future a more complex spawn method will be implemented.
        chunk = self.chunks.random()
        return (chunk, chunk.get_random_position())
        