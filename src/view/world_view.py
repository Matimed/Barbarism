import gc
from lib.abstract_data_types import Matrix
from lib.abstract_data_types import Graph
from lib.chunk import Chunk
from lib.position import Position
from src.events import Tick
from src.references import Layer
from src.view.sprites import CellSprite


class WorldView:
    def __init__(self, event_dispatcher, world_model, window, max_loaded_chunks=30):
        self.ed = event_dispatcher

        self.world_model = world_model

        self.window = window

        self.renderized_sprites = dict() # {Position: {Layer: Sprite}}
        self.renderized_chunks = Graph()

        # It is the maximum amount of chunks that a subscriber 
        # can have loaded at the same time before being eliminated.
        self.max_loaded_chunks = max_loaded_chunks

        CellSprite.set_size(CellSprite.get_min_size())
        CellSprite.set_event_dispatcher(event_dispatcher)


    def render_chunks(self, subscriber, chunks:set):
        """ Receives a Chunk and its subscriber(any object) and render it.
        """

        for chunk in chunks:
            if not self.renderized_chunks.has_node(chunk):
                self._render_cells(chunk)
            self.renderized_chunks.add_edge((subscriber, chunk))


    def get_adjacent_chunks(self, chunks:list):
        """ Receives a list of Chunks and its subscriber (any object)
            and render the Chunks and all its neighbors.
        """
    
        adyacent_chunks = set(chunks)
        for chunk in chunks:
            adyacent_chunks |= set([
                adyacent_chunk for adyacent_chunk 
                in self.world_model.get_adjacent_chunks(chunk)
            ])

        return adyacent_chunks


    def set_renderized_chunks(self, subscriber, chunks:set):
        if self.renderized_chunks.has_node(subscriber):
            render_chunks = tuple(
                self.renderized_chunks.get_adjacencies(subscriber)
            )
            for chunk in render_chunks:
                if chunk not in chunks:
                    self.renderized_chunks.remove_edge((subscriber, chunk))
           
        self.render_chunks(subscriber, chunks)
        
        if (len(self.renderized_chunks.get_empty_nodes()) >
            self.max_loaded_chunks):
            
            self.delete_orphan_chunks()


    def remove_chunks(self, chunks: list):
        """ Removes a chunk from the renderized_chunks
            Graph and the renderized_sprites dictionary.
        """

        for chunk in chunks:
            [self.renderized_sprites.pop(pos) for pos in chunk]


    def delete_orphan_chunks(self):
        """ It checks if there are elements in the graph 
            that do not have connections and removes them 
            from it and from the sprite dictionary.
        """

        orphans = self.renderized_chunks.get_empty_nodes()
        if orphans:
            chunks = list()
            for orphan in orphans:
                try:
                    # We apply the duck test to verify if they are chunks:
                    if orphan.get_random_position: chunks.append(orphan) 
                except AttributeError:
                    continue
            
            self.remove_chunks(chunks)
            self.renderized_chunks.remove_empty_nodes()
            gc.collect()
            


    def get_cells(self, positions: iter):
        """ Receives an iterable of positions and returns the cells in it.
        """
        
        # We use list comprehension in this case because
        # even if the procedure is less clear, it increases performance. 

        return {
            position: self.renderized_sprites[position]
            for position in positions
            }


    def validate_origin(self, origin: tuple, length: tuple) -> (Chunk, Position):
        """ Given an origin point and a length of Matrix, 
            it returns the closest valid Position and its Chunk 
            (or the same one passed by parameter if it is valid).
        """

        limit = self.world_model.get_limit()
        while origin[0] < 0: origin[0] += 1
        while origin[1] < 0: origin[1] +=1

        while (origin[0] + length[0]-1) > limit[0]: origin[0] -= 1
        while (origin[1] + length[1]-1) > limit[1]: origin[1] -= 1

        return self.world_model.get_position(origin)
    

    def complete_cells(self, subscriber, positions: Matrix, origin: Position, desired_length: tuple):
        """ It receives a subscriber, a Matrix of Position objects, 
            a Position of origin and a desired length. 
            And mutates the matrix to the given length and
            containing all the remaining positions.
            It also renders the Chunks adjacent to all those it passes through
            (for that the subscriber is needed).
        """

        new_sprites = dict()
        chunks = set()
        while positions.length() != desired_length:
            first_position = positions.get_element((0,0))

            if first_position != origin:

                if  first_position[0] > origin[0]:
                    last_positions = positions.get_row(0)
                    new_chunks, new_positions = self._find_parallel_positions(
                        last_positions, 0, -1
                        )

                    positions.insert_row(0, new_positions)
                
                elif first_position[1] > origin[1]:
                    last_positions = positions.get_column(0)
                    new_chunks, new_positions = self._find_parallel_positions(
                        last_positions, 1, -1
                        )

                    positions.insert_column(0, new_positions)

            elif positions.length()[0] < desired_length[0]:
                last_positions = positions.get_row(
                    positions.get_last_index()[0]
                    )

                new_chunks, new_positions = self._find_parallel_positions(
                    last_positions, 0, 1
                    )

                positions.append_row(new_positions)

            elif positions.length()[1] < desired_length[1]:
                last_positions = positions.get_column(
                    positions.get_last_index()[1]
                )

                new_chunks, new_positions = self._find_parallel_positions(
                    last_positions, 1, 1
                )

                positions.append_column(new_positions)

            chunks |= new_chunks
            new_sprites |= self.get_cells(new_positions)
            

        self.set_renderized_chunks(
            subscriber, self.get_adjacent_chunks(chunks)
        )
        self.delete_orphan_chunks()
        return new_sprites


    def replace_cells(self, subscriber, positions: Matrix, origin: Position):
        """ It receives a Matrix of positions that mutates it 
            until the first element of this matrix is the origin.
            It also renders the Chunks adjacent to all those it passes through
            (for that the subscriber is needed).
        """

        first_position = positions.get_element((0,0))

        chunks = set()
        new_sprites = dict()
        removed_sprites = dict()

        while origin != first_position:

            if  first_position[0] > origin[0]:
                last_positions = positions.get_row(0)
                new_chunks, new_positions = self._find_parallel_positions(
                    last_positions, 0, -1
                    )

                positions.insert_row(0, new_positions)
                removed_positions = positions.pop_row(
                    positions.get_last_index()[0]
                    )

            elif first_position[1] > origin[1]:
                last_positions = positions.get_column(0)
                new_chunks, new_positions = self._find_parallel_positions(
                    last_positions, 1, -1
                    )

                positions.insert_column(0, new_positions)
                removed_positions = positions.pop_column(
                    positions.get_last_index()[1]
                    )

            elif first_position[0] < origin[0]:
                last_positions = positions.get_row(
                    positions.get_last_index()[0]
                    )

                new_chunks, new_positions = self._find_parallel_positions(
                    last_positions, 0, 1
                    )
                    
                positions.append_row(new_positions)
                removed_positions = positions.pop_row(
                    positions.get_first_index()[0]
                    )
                
            elif first_position[1] < origin[1]:
                last_positions = positions.get_column(
                    positions.get_last_index()[1]
                    )

                new_chunks, new_positions = self._find_parallel_positions(
                    last_positions, 1, 1
                    )

                positions.append_column(new_positions)
                removed_positions = positions.pop_column(
                    positions.get_first_index()[1]
                    )

            else: return False
            
            first_position = positions.get_element((0,0))

            chunks |= new_chunks
            self.set_renderized_chunks(
                subscriber, self.get_adjacent_chunks(chunks)
            )
            new_sprites |= self.get_cells(new_positions)
            removed_sprites |= self.get_cells(removed_positions)

        
        return new_sprites, removed_sprites


    def _find_parallel_positions(self, positions:list, axis:bool, difference: int) -> list[(Chunk, Position)]:
        """ Returns a list of composed tuples of Chunk and position
            with the row/column after/before the one passed by parameter.
        """
        
        new_positions = []
        new_chunks = set()

        for position in positions:
            position_index  = list(position.get_index())
            position_index[axis] += difference

            position = self.world_model.get_position(position_index)

            new_positions.append(position[1])
            new_chunks.add(position[0])

        return new_chunks, new_positions


    def _render_cells(self, positions:iter):
        """ Receive positions and adds the corresponding CellSprites
            to the renderized objects dictionary.
        """

        biomes = self.world_model.get_cells(positions)

        self.renderized_sprites |= {
            position: {Layer.CELL: CellSprite(position, biomes[position])} 
            for position in positions
            }