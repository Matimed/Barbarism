import pygame as pg
from src.view.sprites.sprite import Sprite



class CharactorSprite(Sprite):
    native_job = None
    job = None 
    native_chips = dict()
    chips = native_chips.copy()

    @classmethod
    def get_native_chip(cls, nation): return cls.native_chips.get(nation)


    @classmethod
    def add_chip(cls, nation, chip):
        cls.native_chips[nation] = chip
        cls.update_chip_size()


    @classmethod
    def update_chip_size(cls):
        """ Scales the image to the given size.
        """

        height = cls.get_actual_size()
            
        for nation in cls.native_chips:
            surface = cls.native_chips[nation]
            new_surface = pg.transform.scale(surface,(height,height))
            cls.chips[nation]= new_surface

    
    @classmethod
    def get_job(cls): pass


    def __init__(self, nation):
        self.nation = nation
        self.image = self.get_image()


    def get_image(self):
        full_image = self.get_chip(self.nation).copy()
        full_image.blit(self.get_job(), (0,0)) 
        return full_image


    @classmethod
    def get_chip(cls, nation): return cls.chips[nation]