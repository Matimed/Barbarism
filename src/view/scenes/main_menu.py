import pygame
from view.scenes import Scene
from events import GlobalEvent as ev


class MainMenu(Scene):
    def __init__(self):
        super().__init__()

        # For now this event will be here to speed up the start of the game. 
        end_scene = pygame.event.Event(ev.END_SCENE.val, scene = MainMenu)
        pygame.event.post(end_scene)


    def notify(self, events):
        for event in list(events):
            pass