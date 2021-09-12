import pygame
from pygame.sprite import Sprite
from position import Position
from view.references import CELL
from events import GlobalEvent as ev


class CellSprite(Sprite):
    def __init__(self, position):

        # Later we should use different images for each type of biome.
        self.biome = [CELL['plain']]
        self.image = self.biome[0]
        self.rect = self.image.get_rect()

        # The cell is only interested in knowing its position
        # to be able to launch it as data for an event.
        self.position = position


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def update(self):
        
        if self.rect.collidepoint(pygame.mouse.get_pos()): 
            if pygame.mouse.get_pressed()[0]:

                cell_pressed = pygame.event.Event(
                    ev.CELL_PRESSED.val, position = self.position
                )
                pygame.event.post(cell_pressed)