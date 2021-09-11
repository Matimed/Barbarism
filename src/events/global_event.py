from events import Event
import pygame


class GlobalEvent(Event):
    EXIT = pygame.QUIT
    CLICK = pygame.MOUSEBUTTONDOWN, 'pos (x (int), y (int))', 'button (int)'