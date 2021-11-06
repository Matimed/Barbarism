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


    def get_positions_around(self, center:Position, area:tuple[int,int]) -> (Matrix):
        """ Recives a center position and returns a Matrix with
            tuples that indicates the positions and chunks in which 
            Chunk they are found in the given area.  The area must be 
            a tuple of the length of the expected matrix.

            Returns:
                area_in_chunk:  Matrix[tuple[Chunk, Position]]
        """

        chunk, origin = self._calculate_origin(center, area)
        area_in_chunk = chunk.verify_area(origin, area)

        if not (area_in_chunk.is_complete()):
            area_in_chunk = self.find_next_collection(0, area_in_chunk)

            if not (area_in_chunk.is_complete()):
                area_in_chunk = self.find_next_collection(1, area_in_chunk)

                if not (area_in_chunk.is_complete()):
                    area_in_chunk = self.find_previous_collection(1, area_in_chunk)

                    if not (area_in_chunk.is_complete()):
                        area_in_chunk = self.find_previous_collection(0, area_in_chunk)


        return area_in_chunk


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
        cell_collection = list()

        for element in positions:
            for cell in self.renderized_objects[element[0]][0]:
                if cell.get_position() == element[1]:
                    cell_collection.append((element[0], cell))

        return cell_collection


    def _calculate_origin(self, center:Position, area: tuple[int,int]) -> tuple[Chunk, Position]:
        
        origin = list(center.get_index())
        limit = list(self.world_model.get_limit().get_index())

        y_distance = (area[0]-1)//2
        x_distance = (area[1]-1)//2
            
        origin[0] -=  y_distance
        origin[1] -=  x_distance

        while origin[0] < 0: origin[0] += 1
        while origin[1] < 0: origin[1] +=1

        while (area[0]+ origin[0]) > limit[0]: origin[0] -= 1
        while (area[1]+ origin[1]) > limit[1]: origin[1] -= 1

        return self.world_model.get_position(origin)


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


    def find_previous_collection(self, axis: bool, positions: Matrix) -> Matrix:
        """ Overwrites the matrix until all columns/rows before the first 
            are replaced by values other than False.
        """

        while positions.get_first_index()[axis] != 0:
            if axis == 1:
                first_collection = positions.get_column(positions.get_first_index()[axis])

            elif axis == 0:
                first_collection = positions.get_row(positions.get_first_index()[axis])

            first_collection = list(filter(bool,first_collection))
            previous_collection =  self._find_parallel_collection(first_collection, axis, -1)
            
            if not previous_collection: return False
        
            index = list(positions.index(first_collection[0]))
            index[axis] -= 1

            for element in previous_collection:
                positions.set_element(index, element)
                index[not axis] += 1
        
        return positions


    def find_next_collection(self, axis: bool, positions: Matrix) -> Matrix:
        """ Overwrites the matrix until all columns/rows after the last 
            are replaced by values other than False.
        """

        while positions.get_last_index()[axis] != positions.length()[axis]-1:
            last_collection = None

            if axis:
                last_collection = positions.get_column(positions.get_last_index()[axis])

            else:
                last_collection = positions.get_row(positions.get_last_index()[axis])

            last_collection = list(filter(bool,last_collection))
            next_collection =  self._find_parallel_collection(last_collection, axis, 1)

            if not next_collection: return False

            index = list(positions.get_first_index())
            index[axis] = positions.index(last_collection[0])[axis] + 1
            
            for element in next_collection:
                positions.set_element(index, element)
                index[not axis] += 1
        
        return positions


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

