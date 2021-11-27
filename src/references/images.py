import pygame


CELL = {
    'plain':pygame.image.load('assets/graphics/plain.png').convert()
}

JOB = {
    'founder':pygame.image.load('assets/graphics/founder.png').convert_alpha()
}

CHIP = {
    'red':pygame.image.load('assets/graphics/red_chip.png').convert_alpha(),
    'blue':pygame.image.load('assets/graphics/blue_chip.png').convert_alpha()
}