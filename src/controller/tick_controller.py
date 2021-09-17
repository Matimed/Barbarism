import pygame


class TickController:
    """ Has the iteration of the game that
        runs at 60 frames per second
    """
    
    def __init__(self, event_controller):
        self.event_controller = event_controller
        
        self.fps = 60
        self.clock = pygame.time.Clock()


    def run(self):
        while True:
            self.event_controller.iterate_events()
            self.clock.tick(60)