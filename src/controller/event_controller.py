import pygame
from events import GlobalEvent


class EventController:
    def __init__(self, logic, scene_manager):
        self.logic = logic
        self.scene_manager = scene_manager


    def iterate_events(self):
        model_events = []
        view_events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.logic.update(model_events)
        self.scene_manager.update(view_events)
        