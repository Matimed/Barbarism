from src.events import Tick
from src.events import Quit
from src.events import Click
from src.events import Wheel
import pygame as pg


class PygameController:
    """ It receives events from pygame, translates them to 
        an event of the Event class, and post them in the EventDispatcher.
    """

    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.iterate_events)
    
    
    def iterate_events(self, event):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.ed.post(Quit())

            if event.type == pg.MOUSEBUTTONUP:
                self.ed.post(Click(event.pos, event.button))

            if event.type == pg.MOUSEWHEEL:
                self.ed.post(Wheel(event.y))