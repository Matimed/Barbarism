import pygame as pg
from lib.toolbox import TextBox

class InputBox(pg.sprite.Sprite):
    """ Rectangle in which text can be entered and accessed.
    """

    def __init__(self, click_event, write_event, event_dispatcher, 
            font, initial_text ='', margin=(5,20), size=(350,50),
            text_color=(255,255,255), box_color=(0,0,0), 
            backspace_sound=None, key_sound=None,):
        super().__init__()

        self.box_surface = pg.Surface(size)
        self.box_surface.fill(box_color)

        self.margin = margin

        text_height = size[1] - margin[1]
        self.text_box  = TextBox(font, '', text_color, text_height)
        self.set_text(initial_text)
        
        self.rect = self.box_surface.get_rect()

        self._selected = False
        self.backspace_sound = backspace_sound
        self.key_sound = key_sound

        event_dispatcher.add(click_event, self.handle_collisions)
        if write_event: event_dispatcher.add(write_event, self.write)


    def handle_collisions(self, event):
        """ It is called every time the click event is triggered
            and returns True if the button was pressed.
        """

        if (self.rect.collidepoint(event.get_pos())
                and event.get_button() == 1):
            self._selected = True

        else: self._selected = False
            

    def write(self, event):
        """ It is called every time the write event is triggered
            and adds the letter from the event to the text.
        """
        text = self.get_text()
        if event.key == pg.K_BACKSPACE:
            self.set_text(text[:-1])
            pg.mixer.Sound.play(self.backspace_sound)

        elif event.key == pg.K_SPACE:
            self.set_text(text + ' ')

        else:
            pg.mixer.Sound.play(self.sounds.key_sound)
            text += event.unicode
            self.set_text(text)


    def draw(self, surface):
        """ Receive a surface and draw the
            surface of the box and the text on it.
        """

        surface.blit(self.box_surface, self.rect)
        self.text_box.get_rect().center = self.get_rect().center
        surface.blit(self.text_box.get_surface(), self.text_box.get_rect())


    def set_text(self, text):
        self.text_box.set_text(text)

        if  not self._verify_text_length(self.text_box):
            self.set_text(text[:-1])


    def get_text(self):
        return self.text_box.get_text()


    def get_rect(self):
        return self.rect


    def _verify_text_length(self, text_box):
        """ Verify that the length of the surface of a text 
            is suitable for the rectangular bottom surface.
        """

        return text_sprite.get_size()[0] < \
            self.box_surface.get_size()[0] - self.margin[0]



