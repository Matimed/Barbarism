import functools as ft
from src.model.charactors import Founder
from src.view.sprites import FounderSprite
from src.references import images as img
from src.references import Layer



class SpriteFactory:
    """ Translates entities of the model to Sprites for use in the view.
    """

    sprite_equivalences = {
        Founder: (Layer.CHARACTOR, FounderSprite)
    }

    chips = iter(img.CHIP.values())
    chip_equivalences = dict()


    @staticmethod
    def get_chip(nation):
        """ Dynamically, as the player looks at certain sprites, 
            an image is assigned to them according to its nation.
        """

        if not SpriteFactory.chip_equivalences.get(nation): 
            SpriteFactory.chip_equivalences[nation] = next(SpriteFactory.chips)
        
        return SpriteFactory.chip_equivalences[nation]


    @staticmethod
    def get_sprite(entity):
        """ Creates and returns a Sprite instance that correspond
            with the class of the object passed by value
        """

        equivalence = SpriteFactory.sprite_equivalences[entity.__class__]

        if equivalence[0] == Layer.CHARACTOR:
            return equivalence[0], equivalence[1](
                SpriteFactory.get_chip(entity.get_nation())) 

        else:
            return equivalence[0], equivalence[1]()


    @staticmethod
    def translate_entity_dict(entities: dict):
        entity_sprites = dict()

        for position in entities:
            layer, sprite = SpriteFactory.get_sprite(entities[position])
            entity_sprites |= {position: {layer: sprite}}

        return entity_sprites