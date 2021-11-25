import random 
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from src.model import BiomesManager


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """

    def __init__(self, size:tuple = (55,100), min_size:tuple = (10,20)):
        self.size = size
        self.positions = self._generate_positions(size)
        self.chunks= self._generate_chunks(min_size, size, self.positions)
        self.cells = self._generate_cells(self.positions)


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


    def _generate_positions(self, size:tuple) -> Matrix:
        """ Generates a Matrix of Position type objects 
            based on the given size.
        """

        return Matrix(
            Position.create_collection((0,0), (size[0] -1 ,size[1] -1))
        )


    def _generate_chunks(self, min_size:tuple, size:tuple, positions:Matrix) -> Matrix:
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        chunk_size = list(min_size)
        for i in range(2):
            while True:
                if not (size[i]%chunk_size[i]):
                    break
                chunk_size[i] +=1

        chunks_amount = (size[0] * size[1]) // (chunk_size[0] * chunk_size[1])

        splited_positions = positions.split(chunks_amount)

        return Matrix(
            [[Chunk(positions, (y,x)) for x, positions in enumerate(row)]
            for y, row in enumerate(splited_positions.iter_rows())]
        )


    def _generate_cells(self, positions:iter) -> dict:
        """ Receives an iterable of Position type objects and
            generate a dict of Biomes with a position as key.
        """
        
        temperatures = sorted({
            BiomesManager.get_temperature(biome) 
            for biome in BiomesManager.get_biomes()
        })

        heat_zones = list()
        for temperature in temperatures:
            heat_zones.append(temperature)

        for temperature in reversed(temperatures):
            heat_zones.append(temperature)

        
        rows_quantity = positions.length()[0]
        rows_per_zone = rows_quantity// len(heat_zones)
        cells = dict()

        rows = positions.iter_rows()
        for temperature in heat_zones:
            for i in range(rows_per_zone):
                for position in next(rows):
                    biomes = BiomesManager.get_biomes(temperature=temperature)
                    cells[position] = random.choice(biomes) 

                

        
        # Add snow to excess positions.
        biomes = BiomesManager.get_biomes(temperature=0)
        cells.update(
            {position:random.choice(biomes) for row in rows for position in row}
        )

        return cells


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
        
        