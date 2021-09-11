from events import Event
import pygame


class GlobalEvent(Event):
    EXIT = pygame.QUIT
    CLICK = pygame.MOUSEBUTTONDOWN, 'pos (x (int), y (int))', 'button (int)'

    GAME_START = pygame.event.custom_type()
    BACK_MENU = pygame.event.custom_type()
    END_SCENE = pygame.event.custom_type(), 'scene (Scene)'