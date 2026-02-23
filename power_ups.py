from random import randint, uniform
from typing import Any

import pygame
from pygame.sprite import Sprite

from get_path import get_path

class ShieldOrb(Sprite):
    """Handles player powerups randomly appearing on screen
       that can also be picked up"""
    
    def __init__(self, ai_game):
        """Player shield powerup"""
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.frames_player_shield = []
        for i in range(1, 6):
            img1 = pygame.image.load(get_path(f'assets/Spnning Orb/Blue/frame {i}.png')).convert_alpha()
            img1 = pygame.transform.scale(img1, (36, 36))
            self.frames_player_shield.append(img1)
        
        # Variables for sprite frames
        self.animation_timer = 0
        self.current_frame = 0
        self.image = self.frames_player_shield[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width) 
        self.rect.y = randint(0, self.settings.screen_height)
        
        # Variables from sprite position and brightness conditions
        self.fading_speed = uniform(1.0, 3.0)
        self.timer_fading = uniform(0, self.fading_speed)
        self.timer_appear_disappear = 0
        self.time_disappear = 3 #10
        self.time_appear = 5 #3
        self.image.set_alpha(0)
        self.brightness = 0

        self.appear = False
        self.playergotshield = False
    
    def update(self, dt):
        """Updates frames"""
        if not self.playergotshield:
            # Animation part, changing frames
            self.animation_timer += 100 * dt
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames_player_shield)
                self.image = self.frames_player_shield[self.current_frame]
            
            # Randomly changes sprite position based on the conditions and increases brightness. 
            self.timer_appear_disappear += dt

            # shield off-screen -> on
            if not self.appear:
                if self.timer_appear_disappear >= self.time_disappear:
                    self.timer_appear_disappear = 0
                    self.appear = True

            # shield on-screen -> off
            if self.appear:
                if  self.timer_appear_disappear >= self.time_appear:
                    self.timer_appear_disappear = 0
                    self.appear = False
        
                    self.rect.x = randint(0, self.settings.screen_width) 
                    self.rect.y = randint(int(self.screen_rect.centery), self.settings.screen_height)

            if self.appear:
                self.timer_fading += dt
                if self.timer_fading >= self.fading_speed:
                    self.brightness = 255
                    self.timer_fading = 0

                elif self.timer_fading >= (self.fading_speed * 0.9):
                    self.brightness = 225

                elif self.timer_fading >= (self.fading_speed * 0.8):
                    self.brightness = 200
                
                elif self.timer_fading >= (self.fading_speed * 0.7):
                    self.brightness = 175   

                elif self.timer_fading >= (self.fading_speed * 0.6):
                    self.brightness = 150
                
                elif self.timer_fading >= (self.fading_speed * 0.5):
                    self.brightness = 125

                elif self.timer_fading >= (self.fading_speed * 0.4):
                    self.brightness = 100

                elif self.timer_fading >= (self.fading_speed * 0.3):
                    self.brightness = 75

                elif self.timer_fading >= (self.fading_speed * 0.2):
                    self.brightness = 50
                
                elif self.timer_fading >= (self.fading_speed * 0.1):
                    self.brightness = 25
                
                self.image.set_alpha(self.brightness)
        

    def blitme(self):
        """Draws on screen"""
        if not self.playergotshield:
            if self.appear:
                self.screen.blit(self.image, self.rect)


class ShieldBar(Sprite):
    """Class to represent shield bar percentage for the player"""

    def __init__(self, ai_game):
        """Initialize stats""" 
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.sb = ai_game.sb

        self.image = pygame.image.load(get_path('assets/shieldbar.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (21, 8))
        self.rect = self.image.get_rect()

        self.rect.left = self.screen_rect.left
        self.rect.centery = self.sb.highest_level_rect.centery


class PlayerShield():
    """Class to represent Player shield percentage for the player"""

    def __init__(self, ai_game):
        """Initialize stats""" 
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.sb = ai_game.sb
        self.ship = ai_game.ship
        self.stats = ai_game.stats
        self.shieldorb = ai_game.shieldorb

        self.image = pygame.image.load(get_path('assets/playershield.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        self.shieldup = False
    
    def update(self):
        """Update the shields position relative to the ship's"""
        self.rect.center = self.ship.rect.center

        if self.stats.shield_hits_limit == 0:
            self.shieldup = False
            self.shieldorb.playergotshield = False
            self.stats.shield_hits_limit = self.settings.shield_hits_limit


    def blitme(self):
        """Draws the player shield on ship"""
        if self.shieldup:
            self.screen.blit(self.image, self.rect)


        

        