import pygame as pg
from pygame.sprite import Sprite
from events import Tick
from events import CellPressed
from view.references import CELL


class CellSprite(Sprite):
    ed = None # EventDispatcher

    @staticmethod
    def set_event_dispatcher(event_dispatcher):
        CellSprite.ed = event_dispatcher


    @classmethod
    def get_event_dispatcher(cls):
        return cls.ed


    def __init__(self, position):
        self.get_event_dispatcher().add(Tick, self.update)

        # Later we should use different images for each type of biome.
        self.biome = [CELL['plain']]
        self.image = self.biome[0]
        self.rect = self.image.get_rect()

        # The cell is only interested in knowing its position
        # to be able to launch it as data for an event.
        self.position = position


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def update(self, event):
        if self.rect.collidepoint(pg.mouse.get_pos()): 
            if pg.mouse.get_pressed()[0]:
                self.get_event_dispatcher().post(CellPressed(self.position))