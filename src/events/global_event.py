from events import Event
import pygame


class GlobalEvent(Event):
    EXIT = pygame.QUIT
    CLICK = pygame.MOUSEBUTTONDOWN, 'pos (x (int), y (int))', 'button (int)'

    GAME_START = pygame.event.custom_type()
    BACK_MENU = pygame.event.custom_type()
    END_SCENE = pygame.event.custom_type(), 'scene (Scene)'

    # In the future this event will also have to send a dict of biomes.
    WORLD_GENERATED = pygame.event.custom_type(), 'positions (2D Position array)'
    CELL_PRESSED = pygame.event.custom_type(), 'position (Position)'