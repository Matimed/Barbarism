from events import Tick
from weak_bound_method import WeakBoundMethod as Wbm
import pygame


class PygameController:
    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.ed.add(Tick, Wbm(self.iterate_events))

    
    def iterate_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()