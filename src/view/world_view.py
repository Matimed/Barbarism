from pygame.sprite import AbstractGroup
from src.view.sprites import CellSprite
from src.events import Tick
from lib.abstract_data_types import Matrix
from lib.abstract_data_types import Graph


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


    def get_cells_around(self, chunk, position, area:tuple[int,int]):
        """ Recives a position and its chunk and returns a Matrix with
            all the CellSprites found around it in the given area 
            The area must be a tuple of the length of the expected matrix.
        """


    def _find_collection(self, collection:list, axis:bool, difference: int) -> list[tuple[Chunk, Position]]:
        """ Returns a list of composed tuples of Chunk and position
            with the row/column after/before the one passed by parameter.
        """
        
        new_collection = []
        for element in collection:
            index  = list(element[1].get_index())
            index[axis] += difference
            new_collection.append(self.world_model.get_position(index))
        
        return new_collection



        # raise NotImplementedError


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

