from random import randint, uniform

import pygame
from pygame.sprite import Sprite

from get_path import get_path

class Star(Sprite):
    """Space star asset"""

    def __init__(self, ai_game):
        """Star stuff"""
        super().__init__()

        self.image = pygame.image.load(get_path('assets/stars1.png'))
        self.rect = self.image.get_rect()

        self.settings = ai_game.settings

        self.twinkle_speed = uniform(1.0, 3.0)
        self.timer = uniform(0, self.twinkle_speed)
        self.image.set_alpha(0)
        self.brightness = 0


    def update(self, dt):
        """Update stars"""
        self.timer += dt

        if self.timer >= self.twinkle_speed:
            self.brightness = 255
            self.timer = 0

            self.rect.x = randint(0, self.settings.screen_width)
            self.rect.y = randint(0, self.settings.screen_height)

        elif self.timer >= (self.twinkle_speed * 0.9):
            self.brightness = 225

        elif self.timer >= (self.twinkle_speed * 0.8):
            self.brightness = 200
        
        elif self.timer >= (self.twinkle_speed * 0.7):
            self.brightness = 175   

        elif self.timer >= (self.twinkle_speed * 0.6):
            self.brightness = 150
        
        elif self.timer >= (self.twinkle_speed * 0.5):
            self.brightness = 125

        elif self.timer >= (self.twinkle_speed * 0.4):
            self.brightness = 100

        elif self.timer >= (self.twinkle_speed * 0.3):
            self.brightness = 75

        elif self.timer >= (self.twinkle_speed * 0.2):
            self.brightness = 50
        
        elif self.timer >= (self.twinkle_speed * 0.1):
            self.brightness = 25
        

        self.image.set_alpha(self.brightness)
        
