import pygame as pg
from src.controller import TickController
from src.controller import EventDispatcher
from src.controller import PygameController
from src.events import Quit
from src.model import Logic
from src.view import SceneManager


class Main:
    """ Initializes the game and execute it.
    """
    
    def __init__(self):        
        ed = EventDispatcher()
        ed.add(Quit, self.exit)

        self.tick_controller = TickController(ed)
        self.pygame_event_catcher = PygameController(ed)
        self.scene_manager = SceneManager(ed)
        self.logic = Logic(ed)

        self.run()

    def exit(self, event):
        pg.quit()
        exit()


    def run(self):
        self.tick_controller.run()


