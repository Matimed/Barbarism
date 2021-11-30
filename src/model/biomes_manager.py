import random
from src.references.biome import Biome

class BiomesManager:

    biomes = dict()
    
    @staticmethod
    def detail_biome(temperature:int, ocurrence:float=1, friction:float=0.1, passable=True) -> dict:
        """ Returns a dictionary containing all the given parameters.

            Parameters:
                temperature:  Is used to order it in its generation.
                
                ocurrence:  Probability of occurrence when random is called.
                
                friction:   Range from 0 to 1 that indicates how much it costs
                    the characters to move through the terrain. 
        """

        return {
            'temperature':temperature,
            'ocurrence':ocurrence,
            'friction':friction,
            'passable':passable,
        }
    
    #We declare the biomes here and use the .__ func __ () because 
    # it is the best way to call a static method from the class body.
    biomes = {
        Biome.SNOW: detail_biome.__func__(temperature=0, ocurrence=0.4, friction=0.8,),
        Biome.TUNDRA: detail_biome.__func__(temperature=0, ocurrence=0.3,),
        Biome.GRASS: detail_biome.__func__(temperature=1, ocurrence=1,),
        Biome.FLOWERED: detail_biome.__func__(temperature=1, ocurrence=0.1,),
        Biome.OCEAN: detail_biome.__func__(temperature=1, ocurrence=0.1,passable=False),
        Biome.SAVANNA: detail_biome.__func__(temperature=2, ocurrence=0.3,),
        Biome.DESERT: detail_biome.__func__(temperature=2, ocurrence=0.4,),
    }   
   

    @classmethod
    def get_temperature(cls, biome): return cls.biomes[biome]['temperature']


    @classmethod
    def get_ocurrence(cls, biome): return cls.biomes[biome]['ocurrence']


    @classmethod
    def get_friction(cls, biome): return cls.biomes[biome]['friction']


    @classmethod
    def get_passable(cls, biome): return cls.biomes[biome]['passable']


    @classmethod
    def get_biomes(cls, temperature=None, friction=None, ocurrence=None):
        """ Returns the list of biomes that satisfy all the conditions.
        """

        biomes = cls.biomes.keys()
        if friction != None:
            biomes = [
                biome for biome in biomes 
                if cls.get_friction(biome) == friction
                ]

        if temperature != None:
            biomes = [
                biome for biome in biomes 
                if cls.get_temperature(biome)== temperature
                ]

        if ocurrence != None:
            biomes = [
                biome for biome in biomes 
                if cls.get_ocurrence(biome)== temperature
                ]

        return biomes


    @classmethod
    def select_random(cls, biomes:list):
        """Given a list of biomes choose one at random
            based on their occurrences.
        """
        options = list()
        for biome in biomes:
            options.extend([biome] * int(cls.get_ocurrence(biome) * 100))
        return random.choice(options)