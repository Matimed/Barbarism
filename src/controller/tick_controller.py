import pygame as pg
from src.events import Tick


class TickController:
    """ Has the iteration of the game that
        runs at 60 frames per second
    """
    
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.fps = 60
        self.clock = pg.time.Clock()


    def run(self):
        while True:
            self.ed.post(Tick())
            self.clock.tick(60)