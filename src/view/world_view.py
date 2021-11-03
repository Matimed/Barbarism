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
            area_in_chunk = self._find_next_rows(area_in_chunk)

            if not (area_in_chunk.is_complete()):
                area_in_chunk = self._find_next_columns(area_in_chunk)

                if not (area_in_chunk.is_complete()):
                    area_in_chunk = self._find_previous_columns(area_in_chunk)

                    if not (area_in_chunk.is_complete()):
                        area_in_chunk = self._find_previous_rows(area_in_chunk)


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
                    cells.set_element(cell_index, cell)

        return cells


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

            chunk_index = list(element[0].get_index())
            chunk_index[axis] += difference
            
            new_collection.append(self.world_model.get_position_by_chunk(position_index, chunk_index))
        
        return new_collection


    def _find_previous_columns(self, positions:Matrix) -> Matrix:
        """ Overwrites the matrix until all columns before the first 
            are replaced by values other than False.
        """

        while positions.get_first_index()[1] != 0:
            first_column = positions.get_column(positions.get_first_index()[1])
            first_column = list(filter(bool,first_column))
            previous_column =  self._find_parallel_collection(first_column, 1, -1)


            index = list(positions.index(first_column[0]))
            index[1] -= 1
            
            for element in previous_column:
                positions.set_element(index, element)
                index[0] += 1
        
        return positions


    def _find_previous_rows(self, positions:Matrix) -> Matrix:
        """ Overwrites the matrix until all rows before the first 
            are replaced by values other than False.
        """

        while positions.get_first_index()[0] != 0:
            first_row = positions.get_row(positions.get_first_index()[0])
            first_row = list(filter(bool,first_row))
            previous_row =  self._find_parallel_collection(first_row, 0, -1)

            index = list(positions.index(first_row[0]))
            index[0] -= 1
            
            for element in previous_row:
                positions.set_element(index, element)
                index[1] += 1
        
        return positions


    def _find_next_columns(self, positions:Matrix) -> Matrix:
        """ Overwrites the matrix until all columns after the last 
            are replaced by values other than False.
        """

        while positions.get_last_index()[1] != positions.length()[1]-1:
            last_column = positions.get_row(positions.get_last_index()[1])
            last_column = list(filter(bool,last_column))
            next_column =  self._find_parallel_collection(last_column, 0, 1)


            index = list(positions.get_first_index())
            index[1] = positions.index(last_column[0])[1] + 1
            
            for element in next_column:
                positions.set_element(index, element)
                index[0] += 1
        
        return positions


    def _find_next_rows(self, positions:Matrix) -> Matrix:
        """ Overwrites the matrix until all rows after the last 
            are replaced by values other than False.
        """


        while positions.get_last_index()[0] != (positions.length()[0]-1):
            last_row = positions.get_row(positions.get_last_index()[1])
            last_row = list(filter(bool,last_row))
            next_row =  self._find_parallel_collection(last_row, 1, 1)


            index = list(positions.get_first_index())
            index[0] = positions.index(last_row[0])[0] + 1
            
            for element in next_row:
                positions.set_element(index, element)
                index[1] += 1
        
        return positions


    def _render_cells(self, chunk):
        """ Receive a Chunk and render the suitable CellSprite objects Matrix.
        """

        renderized_cells = Matrix()

        for y, row in enumerate(chunk.copy_matrix().iter_rows()):
            cell_row = []
            for x, position in enumerate(row):
                cell_sprite = CellSprite(position)
                self.ed.add(Tick, cell_sprite.update)

                cell_row.append(cell_sprite)

            renderized_cells.append_row(cell_row)

        if self.renderized_objects.get(chunk):
            self.renderized_objects[chunk][0] = renderized_cells
        else:
            self.renderized_objects[chunk] = list()
            self.renderized_objects[chunk].append(renderized_cells)

