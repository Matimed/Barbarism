import pygame as pg
from src.references import Biome


JOB = {
    'founder':pg.image.load('assets/graphics/charactors/founder.png').convert_alpha(),
    'warrior':pg.image.load('assets/graphics/charactors/warrior.png').convert_alpha(),
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
