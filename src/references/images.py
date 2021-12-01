import pygame as pg
from src.references import Biome


JOB = {
    'founder':pg.image.load('assets/graphics/charactors/founder.png').convert_alpha()
}

CHIP = {
    'filling':pg.image.load('assets/graphics/charactors/filling.png').convert_alpha(),
    'edges':pg.image.load('assets/graphics/charactors/edges.png').convert_alpha()
}

CELL = {
    Biome.DESERT:pg.image.load('assets/graphics/biomes/desert.png').convert(),
    Biome.FLOWERED:pg.image.load('assets/graphics/biomes/flowered.png').convert(),
    Biome.GRASS:pg.image.load('assets/graphics/biomes/grass.png').convert(),
    Biome.TUNDRA:pg.image.load('assets/graphics/biomes/tundra.png').convert(),
    Biome.SAVANNA:pg.image.load('assets/graphics/biomes/savanna.png').convert(),
    Biome.SNOW:pg.image.load('assets/graphics/biomes/snow.png').convert(),
    Biome.OCEAN:pg.image.load('assets/graphics/biomes/ocean.png').convert(),
}

TORCH_BUTTON = {
    'left':pg.image.load('assets/graphics/buttons/torch_button/text_button_left.png').convert_alpha(),
    'middle':pg.image.load('assets/graphics/buttons/torch_button/text_button_middle.png').convert_alpha(),
    'right':pg.image.load('assets/graphics/buttons/torch_button/text_button_right.png').convert_alpha(),
    'right_pressed':pg.image.load('assets/graphics/buttons/torch_button/text_button_right_pressed.png').convert_alpha()
}

ARROW_BUTTON = {
    'unpressed':pg.image.load('assets/graphics/buttons/arrow_button/arrow_button_unpressed.png').convert_alpha(),
    'pressed':pg.image.load('assets/graphics/buttons/arrow_button/arrow_button_pressed.png').convert_alpha()
}

