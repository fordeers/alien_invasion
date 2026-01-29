import pygame.font

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_colour = (0, 135, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48, False, True)

        self._prep_msg(msg)

        # Build the buttons rect based on the given message(msg)
        self.rect = pygame.Rect(0, 0, self.msg_image_rect.width, self.msg_image_rect.height)
        self.rect = self.msg_image_rect
    
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour, 
                self.settings.bg_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center
    
    def draw_button(self):
        """Draw a blank button and then draw message"""
        self.screen.fill(self.button_colour, self.msg_image_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
