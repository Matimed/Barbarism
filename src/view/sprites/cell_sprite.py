from pygame.sprite import Sprite
from view.references import CELL


class CellSprite(Sprite):
    def __init__(self, position):
        # Later we should use different images for each type of biome.
        self.biome = [CELL['plain']]
        self.image = self.biome[0]
        self.rect = self.image.get_rect()
        self.position = position


    def get_rect(self):
        return self.rect