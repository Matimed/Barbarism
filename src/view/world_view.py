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

        self.renderized_objects = {}
        self.renderized_chunks = Graph()


    def add_render_chunks(self, subscriber, chunk):
        """ Adds a chunk with his respective 
            subscriber to the renderized_chunks graph
        """

        self.renderized_chunks.add_edge((subscriber, chunk))
        self.set_renderized_cells(chunk)


    def render_adjacent_chunks(self, subscriber, chunk):
        """ Receives a chunk and link the subscriber with 
            all the chunks adjacent to it.
        """

        for chunk in self.world_model.get_adjacent_chunks(chunk):
            self.add_render_chunks(subscriber, chunk)


    def remove_chunks(self, chunks: list):
        """ Removes a chunk from the renderized_chunks
            Graph and the renderized_objects dictionary.
        """

        for chunk in chunks:
            self.renderized_chunks.remove_node(chunk)
            self.renderized_objects.pop(chunk)

    
    def set_renderized_cells(self, chunk):
        """ Adds to the renderized_cells dictionary the passed chunk 
            as key and associates it with a Matrix of Cell_sprite objects.
        """        

        renderized_cells = Matrix()

        for y, row in enumerate(chunk.copy_matrix().iter_rows()):
            cell_row = []
            for x, position in enumerate(row):
                cell_sprite = CellSprite(position)
                self.ed.add(Tick, cell_sprite.update)

                cell_row.append(cell_sprite)

            renderized_cells.append_row(cell_row)

        self.renderized_objects[chunk] = renderized_cells