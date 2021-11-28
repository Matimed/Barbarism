import colorsys
import pygame as pg
import random
from src.model.charactors import Founder
from src.view.sprites import FounderSprite
from src.view.sprites import CharactorSprite 
from src.references import images as img
from src.references import Layer



class SpriteFactory:
    """ Translates entities of the model to Sprites for use in the view.
    """

    sprite_equivalences = {
        Founder: (Layer.CHARACTOR, FounderSprite)
    }

    hue = random.random()


    @staticmethod
    def hsv_to_color(hue, saturation, value) -> pg.Color:
        return pg.Color(tuple(
            round(i * 255) for i in colorsys.hsv_to_rgb(hue, saturation, value)
        ))


    @classmethod
    def get_new_color(cls):
        cls.hue += 0.618033988749895 # Golden ratio
        cls.hue %= 1
        return cls.hue


    @staticmethod
    def paint(surface, rgb_color):
        new_surface = surface.copy()
        w, h = new_surface.get_size()
        r, g, b, _ = rgb_color
        for x in range(w):
            for y in range(h):
                a = new_surface.get_at((x, y))[3]
                new_surface.set_at((x, y), pg.Color(r, g, b, a))
        
        return new_surface


    @classmethod
    def set_chip(cls, nation):
        """ Dynamically, as the player looks at certain sprites, 
            an image is assigned to them according to its nation.
        """
        
        if not CharactorSprite.get_native_chip(nation): 
            color = cls.get_new_color()
            primary_color = cls.hsv_to_color(color, 0.7, 0.95)
            secundary_color = cls.hsv_to_color(color, 0.7, 0.5)

            filling = cls.paint(img.CHIP['filling'], primary_color) 
            edges = cls.paint(img.CHIP['edges'], secundary_color) 

            filling.blit(edges, (0,0))

            CharactorSprite.add_chip(nation, filling)


    @classmethod
    def get_sprite(cls, entity):
        """ Creates and returns a Sprite instance that correspond
            with the class of the object passed by value
        """

        equivalence = cls.sprite_equivalences[entity.__class__]

        if equivalence[0] == Layer.CHARACTOR:
            cls.set_chip(entity.get_nation())
            return equivalence[0], equivalence[1](entity.get_nation()) 

        else:
            return equivalence[0], equivalence[1]()


    @classmethod
    def translate_entity_dict(cls, entities: dict):
        entity_sprites = dict()

        for position in entities:
            layer, sprite = cls.get_sprite(entities[position])
            entity_sprites |= {position: {layer: sprite}}

        return entity_sprites