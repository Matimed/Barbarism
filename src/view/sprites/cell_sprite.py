import pygame as pg
from src.events import CellPressed
from src.events import Tick
from src.references import Biome
from src.references.images import CELL
from src.view.sprites.sprite import Sprite

class CellSprite(Sprite):
    native_biomes = {biome:CELL[biome] for biome in Biome}
    biomes = native_biomes.copy()
    
    # native_biomes keep the original size in order to 
    # not to lose image quality.


    @classmethod
    def update_size(cls):
        """ Scales all the images to the given size.
        """

        height = cls.get_actual_size()

        for biome in cls.native_biomes:
            surface = cls.native_biomes[biome]
            new_surface = pg.transform.scale(surface,(height,height))
            cls.biomes[biome]= new_surface


    @classmethod
    def get_biome(cls, biome) -> list:
        """ Returns the list of biomes (Surfaces).
        """

        return cls.biomes[biome]


    def __init__(self, position, biome):
        self.biome = biome
        self.image = CellSprite.get_biome(biome)
        self.rect = self.image.get_rect()

        Sprite.get_event_dispatcher().add(Tick, self.routine_update)

        # The cell is only interested in knowing its position
        # to be able to launch it as data for an event.
        self.position = position
        self.update_size()


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
        
        self.image = self.get_biome(self.biome)
        self.rect = self.image.get_rect()

    
    def get_position(self): return self.position


    def __hash__(self):
        return hash(self.position)