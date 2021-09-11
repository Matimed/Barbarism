class Main:
    """ Initializes the game and execute it."""
    
    def __init__(self):
        scene_manager = SceneManager()
        logic = Logic()
        event_controller = EventController(logic, scene_manager)
        self.tick_controller = TickController(event_controller)


    def run(self):
        self.tick_controller.run()

    
if __name__ == '__main__':
    import pygame
    pygame.init()
    from controller import EventController
    from controller import TickController
    from view import SceneManager
    from model import Logic
    
    main = Main()
    main.run()