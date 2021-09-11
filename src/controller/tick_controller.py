import pygame


class TickController:
    def __init__(self, event_controller):
        self.event_controller = event_controller
        
        self.fps = 60
        self.clock = pygame.time.Clock()


    def run(self):
        while True:
            self.event_controller.iterate_events()
            self.clock.tick(60)