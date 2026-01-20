from random import randint

import pygame
from pygame.sprite import Sprite

class SpaceDrop(Sprite):
    """A class to manage spacedrops in background"""

    def __init__(self, ai_game):
        """Create the spacedrop from top screen"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = (230, 230, 230)

        self.rect = pygame.Rect(0, 0, 1, 15)
        self.rect.top = ai_game.screen_get_rect.top

        self.y = float(self.rect.y)

    def update(self, dt):
        """Move the spacedrop down the screen"""
        self.y += 1 * dt

        self.rect.y = self.y

        self.rect.x = randint(0, self.settings.screen_width)
        self.rect.y = randint(0, self.settings.screen_height)

        



    def draw_space_drops(self):
        """Draw the spacedrops on the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)
    