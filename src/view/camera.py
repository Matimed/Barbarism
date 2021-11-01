from lib.abstract_data_types import Matrix


class Camera:
    def __init__(self, event_dispatcher, window, world_view):
        self.window = window

        self.world_view = world_view

        self.visible_cells = Matrix()
        self.visible_chunks = list()


        self.origin = (0,0)

        # Minimum harcoded size for the cells matrix. 
        self.min_length = (5,3)
        self.max_length = self._calculate_length(CellSprite.get_min_size())



    def set_visible_chunks(self, chunks):
        """ Replace the list of visible chunks for a new one. 
        """
        
        self.visible_chunks = chunks


    def set_visible_cells(self, cells):
        """ Replace the Matrix of visible cells for a new one 
            and recalculates the origin point.
        """

        self.visible_cells = cells
        self.origin = self._get_new_origin()


    def _get_new_origin(self):
        """ Calculates and returns the point 
            from which the cells should be drawn,
            based on the resolution, the zoom and the matrix length.
        """

        resolution = self.window.get_resolution()
        cell_size = CellSprite.get_actual_size()
        lenght = self.visible_cells.length()

        margins = (
            resolution[0] - (lenght[0] * cell_size),
            resolution[1] - (lenght[1] * cell_size)
            )

        origin = (margins[0] // 2, margins[1] // 2)        

        return origin


    def _calculate_length(self, cells_size:int ) -> tuple[tuple, tuple]:
        """ Returns the length that the visible_cells should have,
            based on the given size of the CellSprites.
        """

        resolution = self.window.get_resolution()

        return (resolution[0] // cells_size, resolution[1] // cells_size)

