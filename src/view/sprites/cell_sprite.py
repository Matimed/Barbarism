import pygame as pg
from src.events import Tick
from src.events import CellPressed
from src.view.references import CELL


class CellSprite(pg.sprite.Sprite):
    ed = None # EventDispatcher
    min_size = 50


    # Later we should use different images for each type of biome.
    native_biomes = [CELL['plain']]
    biomes = native_biomes.copy()
    
    # native_biomes keep the original size in order to 
    # not to lose image quality.
    
   
    @staticmethod
    def set_event_dispatcher(event_dispatcher):
        CellSprite.ed = event_dispatcher


    @classmethod
    def set_size(cls, height:int):
        """ Scales all the images to the given size.
        """

        assert height >= cls.min_size, "Size must be larger than minimum."

        for i, surface in enumerate(cls.native_biomes):
            new_surface = pg.transform.scale(surface,(height,height))
            cls.biomes[i]= new_surface


    @classmethod
    def get_event_dispatcher(cls):
        return cls.ed


    @classmethod
    def get_min_size(cls) -> int:
        return cls.min_size


    @classmethod
    def get_actual_size(cls) -> int:
        """ Returns the current height of the surface.
        """

        return cls.biomes[0].get_size()[0]


    @classmethod
    def get_biomes(cls) -> list:
        """ Returns the list of biomes (Surfaces).
        """

        return cls.biomes


    def __init__(self, position):
        self.biome = 0
        self.image = CellSprite.get_biomes()[self.biome]
        self.rect = self.image.get_rect()

        CellSprite.get_event_dispatcher().add(Tick, self.routine_update)

        # The cell is only interested in knowing its position
        # to be able to launch it as data for an event.
        self.position = position


    def draw(self, surface):
        """ Receives a surface and is drawn on it.
        """

        surface.blit(self.image, self.rect)


    def routine_update(self, event):
        """ Updates the cell state on every Tick.
        """

        pass


    def handle_collisions(self, event):
        """ Checks if the mouse has clicked on it and reacts.
        """

        if self.rect.collidepoint(event.get_pos()) and event.get_button() == 1:
            self.get_event_dispatcher().post(CellPressed(self.position))
            print(self.position)


    def refresh(self):
        """ Replace its Image and Rect with new ones 
            in order to update its information (e.g. size).
        """
        
        self.image = CellSprite.get_biomes()[self.biome]
        self.rect = self.image.get_rect()

    
    def get_position(self): return self.position