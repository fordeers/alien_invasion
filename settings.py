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
        self.ship_speed = 10

        # Alien settings
        self.alien_speed = 2.0
        self.fleet_drop_speed = 30
        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1


        # Bullet
        self.bullet_speed = 4.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (255, 255, 0)
        self.bullets_allowed = 3

    def _exit_fullscreen(self):
        """Exit fullscreen mode"""
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def _fullscreen_mode(self):
        """Fullscreen mode"""
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)