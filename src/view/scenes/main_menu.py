import pygame
from view.scenes import Scene
from events import GlobalEvent as ev


class MainMenu(Scene):
    def __init__(self):
        super().__init__()

        # For now this event will be here to speed up the start of the game. 
        game_start = pygame.event.Event(ev.GAME_START.val)
        pygame.event.post(game_start)


    def notify(self, events):
        for event in list(events):
            if event.type == ev.GAME_START:
                end_scene = pygame.event.Event(ev.END_SCENE.val, scene = MainMenu)
                pygame.event.post(end_scene)