import pygame as pg
from src.events import Tick
from src.references.images import JOB
from src.view.sprites.charactor import CharactorSprite

class WarriorSprite(CharactorSprite):
    native_job = JOB['warrior'] 
    job = native_job.copy()


    @classmethod
    def update_size(cls):
        """ Scales the image to the given size.
        """

        height = cls.get_actual_size()

        surface = cls.native_job
        new_surface = pg.transform.scale(surface,(height,height))
        cls.job = new_surface
        
        cls.update_chip_size()
        
    
    @classmethod
    def get_job(cls): return cls.job


    def __init__(self, chip_image):
        super().__init__(chip_image)

        self.rect = self.image.get_rect()

        WarriorSprite.get_event_dispatcher().add(Tick, self.routine_update)
        self.update_size()


    def routine_update(self, event):
        pass


    def refresh(self):
        """ Replace its Image and Rect with new ones 
            in order to update its information (e.g. size).
        """
        
        self.image = self.get_image()
        self.rect = self.image.get_rect()