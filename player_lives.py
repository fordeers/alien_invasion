import pygame
from pygame.sprite import Sprite

class PlayerLives(Sprite):
    """A class to represent a single player live"""

    def __init__(self, ai_game):
        """Initilize the player live and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.sb = ai_game.sb

        self.image = pygame.image.load('assets/heart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()

        self.rect.left = self.screen_rect.left 
        self.rect.bottom = self.sb.high_score_rect.bottom
    
        
