from events import Tick
import pygame
from events import CellPressed


class PygameController:
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.iterate_events)

    
    def iterate_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

