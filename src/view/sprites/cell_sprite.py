from pygame.sprite import Sprite
from view.references import CELL


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