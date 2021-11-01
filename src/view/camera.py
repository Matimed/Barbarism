from lib.abstract_data_types import Matrix


class Camera:
    def __init__(self, event_dispatcher, window, world_view):
        self.window = window

        self.world_view = world_view

        self.visible_cells = Matrix()
        self.visible_chunks = list()


        self.origin = (0,0)

