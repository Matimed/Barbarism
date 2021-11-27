import pygame as pg


class Sprite(pg.sprite.Sprite):
    ed = None
    min_size = 50
    actual_size = min_size

    @staticmethod
    def set_event_dispatcher(event_dispatcher):
        Sprite.ed = event_dispatcher


    @classmethod
    def get_event_dispatcher(cls):
        return cls.ed


    @staticmethod
    def set_size(height):
        assert height >= Sprite.min_size, "Size must be larger than minimum."
        Sprite.actual_size = height


    @classmethod
    def get_min_size(cls) -> int:
        return cls.min_size


    @classmethod
    def get_actual_size(cls) -> int:
        """ Returns the current height of the surface.
        """

        return cls.actual_size


    def __init__(self):
        self.image = None
        self.rect = None


    def draw(self, surface):
        """ Receives a surface and is drawn on it.
        """

        surface.blit(self.image, self.rect)

    
    def refresh(self):
        """ Replace its Image and Rect with new ones 
            in order to update its information (e.g. size).
        """
        
        self.image = self.get_image()
        self.rect = self.image.get_rect()