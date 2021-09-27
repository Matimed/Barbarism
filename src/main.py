

class Main:
    """ Initializes the game and execute it.
    """
    
    def __init__(self):
        ed = EventDispatcher()
        self.tick_controller = TickController(ed)
        self.pygame_event_catcher = PygameController(ed)
        self.scene_manager = SceneManager(ed)
        self.logic = Logic(ed)


    def run(self):
        self.tick_controller.run()

    
if __name__ == '__main__':
    import pygame
    pygame.init()
    from controller import EventDispatcher
    from controller import TickController
    from controller import PygameController
    from view import SceneManager
    from model import Logic
    
    main = Main()
    main.run()


