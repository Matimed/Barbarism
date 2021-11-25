from src.references.biome import Biome

class BiomesManager:

    biomes = dict()
    
    @staticmethod
    def detail_biome(temperature,friction=1) -> dict:
        """ Returns a dictionary containing all the given parameters.
        """

        return {
            'friction':friction,
            'temperature':temperature
        }
    
    #We declare the biomes here and use the .__ func __ () because 
    # it is the best way to call a static method from the class body.
    biomes = {
        Biome.SNOW: detail_biome.__func__(temperature=0, friction=2),
        Biome.TUNDRA: detail_biome.__func__(temperature=1),
        Biome.GRASS: detail_biome.__func__(temperature=2),
        Biome.FLOWERED: detail_biome.__func__(temperature=2),
        Biome.OCEAN: detail_biome.__func__(temperature=2),
        Biome.SAVANNA: detail_biome.__func__(temperature=3),
        Biome.DESERT: detail_biome.__func__(temperature=4),
    }   
   

    @classmethod
    def get_temperature(cls, biome): return cls.biomes[biome]['temperature']


    @classmethod
    def get_friction(cls, biome): return cls.biomes[biome]['friction']


    @classmethod
    def get_biomes(cls, temperature=None, friction=None):
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

        return biomes
