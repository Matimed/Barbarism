import pygame as pg
from src.references import Biome


JOB = {
    'founder':pg.image.load('assets/graphics/founder.png').convert_alpha()
}

CHIP = {
    'red':pg.image.load('assets/graphics/red_chip.png').convert_alpha(),
    'blue':pg.image.load('assets/graphics/blue_chip.png').convert_alpha()
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
