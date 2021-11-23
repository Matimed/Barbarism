import functools as ft
from src.model.charactors import Founder
from src.view.sprites import FounderSprite


class SpriteFactory:
    """ Translates entities of the model to Sprites for use in the view.
    """

    equivalences = {
        Founder: FounderSprite
    }


    @staticmethod
    @ft.lru_cache(maxsize=None)
    def get_sprite(entity):
        """ Creates and returns a Sprite instance that correspond
            with the class of the object passed by value
        """

        return SpriteFactory.equivalences[entity.__class__]()


    @staticmethod
    def translate_entity_dict(entities: dict):
        entity_sprites = dict()
        
        # We use list comprehension in this case because
        # even if the procedure is less clear, it increases performance. 
        for position in entities:
            entity_sprites |= {
                position: {
                    layer: SpriteFactory.get_sprite(entities[position][layer])
                    }
                for layer in entities[position]}

        return entity_sprites