import pygame as pg
from src.view.sprites.sprite import Sprite


class Charactor(Sprite):
    job_image = None


    @staticmethod
    def get_sized_images(chip_image, job_image):
        """ Scales the image to the given size.
        """

        height = Charactor.get_actual_size()

        sized_chip_image = pg.transform.scale(
            chip_image,(height,height)
            )
        
        sized_job_image = pg.transform.scale(
            job_image,(height,height)
            )
        
        return sized_chip_image, sized_job_image
    

    @classmethod
    def get_job_image(cls): return cls.job_image


    def __init__(self, chip_image):
        self.chip_image = chip_image


    def get_image(self):
        chip_img, job_img = Charactor.get_sized_images(
            self.chip_image, self.get_job_image()
            )
        
        chip_img.blit(job_img, (0,0))

        return chip_img