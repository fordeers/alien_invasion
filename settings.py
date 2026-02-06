import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (10, 10, 20)

        # Ship settings
        self.ship_speed = 270
        self.ship_limit = 3

        # Alien settings
        self.alien_speed = 120.0
        self.fleet_drop_speed = 2000

        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Bullet
        self.bullet_speed = 220.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.side_bullet_width = 15
        self.side_bullet_height = 3
        self.bullet_colour = (13, 255, 0)
        self.bullets_allowed = 5

        # Delta Time FPS
        self.fps = 80

        # How quickly the game speeds up
        self.speedup_scale = 1.3

        # Scoring settings
        self.alien_points = 1
        self.score_scale = 2

        self.initialize_dynamic_settings()
            
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 270
        self.bullet_speed = 220
        self.alien_speed = 120

        # fleet_direction of 1 represents right; -1 respresents left
        self.fleet_direction = 1
        
        self.score_scale = 2
        self.alien_points = 1

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.score_scale = 2
        self.alien_points = self.alien_points * self.score_scale

    def _exit_fullscreen(self):
        """Exit fullscreen mode"""
        pygame.display.set_mode((self.screen_width, self.screen_height))

    def _fullscreen_mode(self):
        """Fullscreen mode"""
        pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)