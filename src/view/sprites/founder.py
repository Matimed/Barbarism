import pygame as pg
from src.events import Tick
from src.references.images import JOB
from src.view.sprites.charactor import Charactor

class FounderSprite(Charactor):
    job_image = JOB['founder']

    def __init__(self, chip_image):
        super().__init__(chip_image)

        self.image = self.get_image()
        self.rect = self.image.get_rect()

        FounderSprite.get_event_dispatcher().add(Tick, self.routine_update)


    def routine_update(self, event):
        pass