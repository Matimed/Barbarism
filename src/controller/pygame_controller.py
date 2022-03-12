import pygame as pg
from src.events import ArrowKey
from src.events import Click
from src.events import Quit
from src.events import Tick
from src.events import Wheel
from src.events import ShiftEnded

class PygameController:
    """ It receives events from pygame, translates them to an event 
        of the Event class, and post them in the EventDispatcher.
    """

    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher
        self.ed.add(Tick, self.iterate_events)
        self.arrow_keys_pressed = dict()

    def iterate_events(self, event):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.ed.post(Quit())

            elif event.type == pg.KEYUP:
                if event.key in self.arrow_keys_pressed:
                    self.arrow_keys_pressed.pop(event.key)
                if event.key == pg.K_n:
                    self.ed.post(ShiftEnded())

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP: 
                    self.arrow_keys_pressed[event.key] = ArrowKey(y=1)
                if event.key == pg.K_DOWN: 
                    self.arrow_keys_pressed[event.key] = ArrowKey(y=-1)
                if event.key == pg.K_RIGHT: 
                    self.arrow_keys_pressed[event.key] = ArrowKey(x=1)
                if event.key == pg.K_LEFT: 
                    self.arrow_keys_pressed[event.key] = ArrowKey(x=-1)
                

            elif event.type == pg.MOUSEBUTTONUP:
                self.ed.post(Click(event.pos, event.button))

            elif event.type == pg.MOUSEWHEEL:
                self.ed.post(Wheel(event.y))
                

        if self.arrow_keys_pressed: 
            [self.ed.post(event) for event in self.arrow_keys_pressed.values()]