import pygame as pg
from lib.toolbox import ArrowButton
from lib.toolbox import InputBox


class NumericSelector(pg.AbstractGroup):
    """ Tool to select in a certain range of numbers.
    """

    def __init__(self, pressed_image, unpressed_image, 
            click_event, event_dispatcher, font, maximum, minimum, 
            box_size=(60,60), text_color=(255,255,255),
            box_color=(0,0,0), sound=None, initial_number=None,):

        
        assert maximum > minimum, \
            'The maximum value cannot be less than or equal to the minimum.'
        
        self.box_size = box_size
        self.maximum = maximum
        self.minimum = minimum
        if initial_number: self.number = initial_number
        else: self.number = minimum

        self.up_button = ArrowButton(
            pressed_image, unpressed_image, 
            click_event, event_dispatcher,
            self.box_size[0], 90, sound
            )

        self.down_button = ArrowButton(
            pressed_image, unpressed_image, 
            click_event, event_dispatcher,
            self.box_size[0], 270, sound
            )

        self.box = InputBox(click_event, None, event_dispatcher, font,
            str(self.number), (10, int(self.box_size[1] * 1/3)),
            self.box_size, text_color, box_color
            )


    def draw(self, surface):
        self.up_button.get_rect().midbottom = (
            self.box.get_rect().midtop[0], 
            self.box.get_rect().midtop[1] - self.box_size[1] / 10
            )

        self.down_button.get_rect().midtop = (
            self.box.get_rect().midbottom[0], 
            self.box.get_rect().midbottom[1] + self.box_size[1] / 10
            )

        self.box.draw(surface)
        self.up_button.draw(surface)
        self.down_button.draw(surface)


    def get_number(self):
        return self.number

    
    def get_rect(self):
        return self.box.get_rect()