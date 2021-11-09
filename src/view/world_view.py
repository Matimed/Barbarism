from pygame.sprite import AbstractGroup
from src.view.sprites import CellSprite
from src.events import Tick
from lib.abstract_data_types import Matrix
from lib.abstract_data_types import Graph
from lib.chunk import Chunk
from lib.position import Position


class WorldView:
    def __init__(self, event_dispatcher, world_model, window):
        self.ed = event_dispatcher

        self.world_model = world_model

        self.window = window

        self.renderized_objects = dict()
        self.renderized_chunks = Graph()

        CellSprite.set_size(CellSprite.get_min_size())
        CellSprite.set_event_dispatcher(event_dispatcher)


    def render_chunk(self, subscriber, chunk):
        """ Receives a Chunk and its subscriber(any object) and render it.
        """

        self.renderized_chunks.add_edge((subscriber, chunk))
        self._render_cells(chunk)


    def render_adjacent_chunks(self, subscriber, chunk):
        """ Receives a Chunk and its subscriber (any object)
            and render the Chunk and all its neighbors.
        """

        self.render_chunk(subscriber, chunk)
        for node in self.world_model.get_adjacent_chunks(chunk):
            self.render_chunk(subscriber, node)


    def remove_chunks(self, chunks: list):
        """ Removes a chunk from the    renderized_chunks
            Graph and the renderized_objects dictionary.
        """

        for chunk in chunks:
            self.renderized_chunks.remove_node(chunk)
            self.renderized_objects.pop(chunk)


    def get_renderized_objects(self, chunk) -> list:
        """ Returns the list of renderized objects for a given Chunk.
        """

        return self.renderized_objects[chunk]

    
    def get_cells(self, positions:Matrix) -> Matrix:
        """ It receives a Matrix of tuples that indicates 
            the positions and chunks in which they are found and 
            returns a Matrix of CellSprite objects with all 
            the requested positions.

            Recives:
                positions:  Matrix[tuple[Chunk, Position]]
        """

        chunks = set([element[0] for element in positions])
        cells = positions.copy()
        for chunk in chunks:
            cells_in_chunk = self.renderized_objects[chunk][0]
            for element in positions:
                if element[0] == chunk:
                    position_index = chunk.get_position_index(element[1])
                    cell = cells_in_chunk.get_element(position_index)
                    cell_index  = positions.index(element)
                    cells.set_element(cell_index, [chunk, cell])

        return cells


    def get_cells_by_list(self, positions: list):
        """ Receives a list of positions (Chunk, Position) and 
            returns the corresponding CellSprite list.
        """
        
        cell_collection = list()

        for element in positions:
            cells = self.renderized_objects[element[0]][0]
            for cell in cells:
                if cell.get_position() == element[1]:
                    cell_collection.append((element[0], cell))

        return cell_collection


    def validate_origin(self, origin: tuple, length: tuple) -> tuple[Chunk, Position]:
        """ Given an origin point and a length of Matrix, 
            it returns the closest valid Position and its Chunk 
            (or the same one passed by parameter if it is valid).
        """

        limit = list(self.world_model.get_limit().get_index())
        while origin[0] < 0: origin[0] += 1
        while origin[1] < 0: origin[1] +=1

        while (origin[0] + length[0]) > limit[0]: origin[0] -= 1
        while (origin[1] + length[1]) > limit[1]: origin[1] -= 1

        return self.world_model.get_position(origin)


    def complete_cells(self, cells: Matrix, origin: Position, desired_length: tuple):
        """ It receives a Matrix of cells (Chunk, CellSprite), 
            a Position of origin and a desired length and 
            returns a Matrix of the given length 
            that contains all the remaining cells.
        """

        while cells.length() != desired_length:
            first_position = cells.get_element((0,0))[1].get_position()
            if first_position != origin[1]:
                
                if  first_position.get_index()[0] < origin[1].get_index()[0]:

                    collection = list()
                    for element in cells.get_row(0):
                        collection.append((element[0], element[1].get_position()))

                    new_positions = self._find_parallel_collection(collection, 0, -1)
                    new_cells = self.get_cells_by_list(new_positions)
                    
                    cells.insert_row(0, new_cells)
                    continue
                
                elif first_position.get_index()[1] < origin[1].get_index()[1]:

                    collection = list()
                    for element in cells.get_column(0):
                        collection.append((element[0], element[1].get_position()))

                    new_positions = self._find_parallel_collection(collection, 1, -1)
                    new_cells = self.get_cells_by_list(new_positions)
                    
                    cells.insert_column(0, new_cells)
                    continue

            elif cells.length()[0] < desired_length[0]:

                collection = list()
                for element in cells.get_row(cells.get_last_index()[0]):
                    collection.append((element[0], element[1].get_position()))

                new_positions = self._find_parallel_collection(collection, 0, 1)
                new_cells = self.get_cells_by_list(new_positions)

                cells.append_row(new_cells)
                continue

            elif cells.length()[1] < desired_length[1]:

                collection = list()
                for element in cells.get_column(cells.get_last_index()[1]):
                    collection.append((element[0], element[1].get_position()))

                new_positions = self._find_parallel_collection(collection, 1, 1)
                new_cells = self.get_cells_by_list(new_positions)
                
                cells.append_column(new_cells)
                continue


        return cells


    def _find_parallel_collection(self, collection:list, axis:bool, difference: int) -> list[tuple[Chunk, Position]]:
        """ Returns a list of composed tuples of Chunk and position
            with the row/column after/before the one passed by parameter.
        """
        
        new_collection = []
        for element in collection:
            position_index  = list(element[1].get_index())
            position_index[axis] += difference

            position = self.world_model.get_position_by_chunk(position_index, element[0].get_index())
            if not position:
                chunk_index = list(element[0].get_index())
                chunk_index[axis] += difference
                position = self.world_model.get_position_by_chunk(position_index,chunk_index)

                if not position: return False
            

            new_collection.append(position)

        return new_collection


    def _render_cells(self, chunk):
        """ Receive a Chunk and render the suitable CellSprite objects Matrix.
        """

        renderized_cells = Matrix()

        for y, row in enumerate(chunk.copy_matrix().iter_rows()):
            cell_row = []
            for x, position in enumerate(row):
                cell_sprite = CellSprite(position)

                cell_row.append(cell_sprite)

            renderized_cells.append_row(cell_row)

        self.renderized_objects.setdefault(
            chunk, list()
            ).append(renderized_cells)

