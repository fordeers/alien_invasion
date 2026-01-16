from random import randint

import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """Space star asset"""

    def __init__(self, ai_game):
        """Star stuff"""
        super().__init__()

        self.image = pygame.image.load('assets/stars1.png')
        self.rect = self.image.get_rect()

        self.settings = ai_game.settings

        self.twinkle_speed = randint(50, 60)
        self.timer = randint(0, 60)
        self.image.set_alpha(0)
        self.brightness = 0


    def update(self):
        """Update stars"""

        self.timer += 1

        if self.timer == (self.twinkle_speed // 3):
            self.brightness = 25

        elif self.timer == (self.twinkle_speed // 2):
            self.brightness = 50
        
        elif self.timer == (self.twinkle_speed // 3):
            self.brightness = 75

        elif self.timer == (self.twinkle_speed // 2):
            self.brightness = 100

        elif self.timer == (self.twinkle_speed // 3):
            self.brightness = 125

        elif self.timer == (self.twinkle_speed // 2):
            self.brightness = 150
        
        elif self.timer == (self.twinkle_speed // 3):
            self.brightness = 175   

        elif self.timer == (self.twinkle_speed // 2):
            self.brightness = 200
        
        elif self.timer == (self.twinkle_speed // 2):
            self.brightness = 225
        
        elif self.timer >= self.twinkle_speed:
            self.brightness = 255
            self.timer = 0

            self.rect.x = randint(0, self.settings.screen_width)
            self.rect.y = randint(0, self.settings.screen_height)

            # self.twinkle_speed = randint(20, 60)


        self.image.set_alpha(self.brightness)
        
