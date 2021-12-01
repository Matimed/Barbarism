import random 
from src.events import MoveEntity
from src.events import WorldUpdated
from lib.abstract_data_types import NonDirectionalGraph
from lib.abstract_data_types import DirectionalGraph
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from src.model import BiomesManager
from src.model.charactors import Charactor


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """
    
    def __init__(self, event_dispatcher, size:tuple = (128,128), min_size:tuple = (20,30), biomes:int=64):
        assert biomes <= 128, \
            "So many biomes take a long time to generate the world"
        
        assert size[0]/2 >= biomes, (
            "The requested number of biomes" 
            "is not very suitable for the size of the map"
        )

        self.ed = event_dispatcher

        self.ed.add(MoveEntity, self.move_charactor)

        self.size = size
        self.positions: Matrix = self._generate_positions(size)
        self.chunks= self._generate_chunks(min_size, size, self.positions)
        self.cells = self._generate_cells(self.positions,biomes)
        self.entities = NonDirectionalGraph() # {Position -- Object}


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

        return self.chunks.get_adjacencies(chunk.get_index())


    def get_adjacent_positions(self, position) -> list:
        """ Returns the list of Position objects 
            adjacent to the one given by parameter.
        """

        return self.positions.get_adjacencies(self.positions.index(position))


    def create_route(self, origin, destination):
        """ Given two Position returns the fastest way
            to get from the origin to the destination point.
        """

        open_set = dict() # {Position: g}
        closed_set = set() # {Position}
        dirty_path = DirectionalGraph()
        
        open_set[origin] = 0
        while open_set:
            fs = dict()
            for position in open_set:
                friction = BiomesManager.get_friction(self.cells[position]) 
                h =  self.positions.manhattan_distance(destination, position)*friction
                fs[h + open_set[position]] = position
            
            winner = fs[min(fs)]

            open_set.pop(winner)
            closed_set.add(winner)

            if winner is destination: break
            
            positions = self.positions.get_adjacencies_without_diagonals(winner)
            for position in positions:
                if position in closed_set: continue
                if self.avoid_position(position): continue

                g = self.positions.manhattan_distance(winner, position)
                
                if position in open_set:
                    if g > open_set[position]:
                        continue

                open_set[position] = g
                dirty_path.add_edge(position, winner)


        if dirty_path.has_node(destination):
            path = list()
            key = {destination}
            while key != set():
                path.append(list(key)[0])
                key = dirty_path.get_adjacencies(list(key)[0])

            return list(reversed(path))[1:]

        else: return None


    def avoid_position(self, position):
        """ Returns True if it's no problem with pass over a position.
        """
        
        if not BiomesManager.get_passable(self.cells[position]): 
            return True

        elif self.entities.has_node(position): 
            for entity in self.entities.get_adjacencies(position):
                entity
                if isinstance(entity, Charactor):
                    return True


        else: return False


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


    def add_entity(self, position, entity):
        self.entities.add_edge((position, entity))


    def get_entities(self, positions: list):
        entities = dict()
        entities |= {
            position: self.entities.get_adjacencies(position)
            for position in positions
            if self.entities.has_node(position)
            }
            
        return entities


    def get_entity(self, position):
        if self.entities.has_node(position):
            return {position: self.entities.get_adjacencies(position)}

        else: return None


    def get_entity_position(self, entity):
        return list(self.entities.get_adjacencies(entity))[0]


    def get_charactor_nation(self, position):
        for nation in self.nations:
            if nation.has_charactor(position):
                return nation


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


    def _generate_cells(self, positions:Matrix, biomes_qty=64) -> dict:
        """ Receives an iterable of Position type objects and
            generate a dict of Biomes with a position as key.
        """
        
        rows = sorted({
            BiomesManager.get_temperature(biome) 
            for biome in BiomesManager.get_biomes()
        })

        heat_zones = list()
        for temperature in rows:
            heat_zones.append(temperature)

        for temperature in reversed(rows):
            heat_zones.append(temperature)

        rows_biome = positions.length()[0]/ biomes_qty
        biomes= dict()
        for i in range (biomes_qty):
            biome = BiomesManager.select_random(BiomesManager.get_biomes())
            temperature = BiomesManager.get_temperature(biome)
            biomes.setdefault(temperature, list())
            biomes[temperature].append(biome)

        rows_temperature = {
            temperature: int((len(biomes[temperature]) * rows_biome) /
            (heat_zones.count(temperature))) for temperature in biomes
        }
        
        seeds = dict()
        seeds_index = dict()
        seed = 1
        while biomes:
            start_row = 0
            stop_row = int(rows_temperature[min(rows_temperature)]-1)
            for i,temperature in enumerate(heat_zones):
                if temperature in biomes and biomes[temperature]:
                    if i != 0:
                        start_row = stop_row
                        stop_row += rows_temperature[temperature]

                    row = positions.get_row(
                        random.randrange(start_row, stop_row)
                    )
                    biome = biomes[temperature].pop()
                    seeds[seed] = biome
                    seeds_index[seed] = (random.choice(row).get_index())
                    seed +=1

                else:
                    if temperature in biomes:
                        biomes.pop(temperature)
                    continue

        sorted_index = [seeds_index[key] for key in sorted(seeds_index)]
        zones = iter(positions.generate_voronoi_tesselation(sorted_index))
        return {position:seeds[next(zones)] for position in positions}


    def generate_spawn_point(self) -> (Chunk, Position):
        """ Returns a Chunk and a Position on that 
            chunk where to place a charactor.
        """

        while True:
            chunk = self.chunks.random()
            position = chunk.get_random_position()
            
            if BiomesManager.get_passable(self.cells[position]):
                return (chunk, position)


    def move_charactor(self, event):
        """ Moves an entity to another position.
            Recives an event with an entity and it's destination.
        """
        charactor = event.get_entity()
        
        # Saves the position of ther charactor.
        past_position = list(self.entities.get_adjacencies(charactor))[0]
        
        # Removes the position of ther charactor and the charactor 
        # from the entities graph.
        self.entities.remove_node(charactor)
        self.entities.remove_empty_nodes()

        # Creates an edge between the charactor and the destination 
        # position in the graph.
        self.entities.add_edge((charactor, event.get_destination()))
        
        self.ed.post(WorldUpdated([past_position, event.get_destination()]))

    
    def get_cells(self, positions:iter):
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """

        return {position:self.cells[position] for position in positions}
        
        
