import pygame
from events import GlobalEvent as ev


class EventController:
    def __init__(self, logic, scene_manager):
        self.logic = logic
        self.scene_manager = scene_manager


    def iterate_events(self):
        model_events = []
        view_events = []

        for event in pygame.event.get():
            if event.type == ev.EXIT:
                pygame.quit()
                exit()

            if event.type == ev.GAME_START:
                view_events.append(event)
                model_events.append(event)

            if event.type == ev.END_SCENE:
                view_events.append(event)

        self.logic.notify(model_events)
        self.scene_manager.notify(view_events)
        