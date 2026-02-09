import pygame


from get_path import get_path

class Earth:
    """Earth Animation"""

    def __init__(self, ai_game):
        """Initialize Earth animation."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.frames = []
        # Load all 60 frames into memory once
        for i in range(119):
            img = pygame.image.load(get_path(f'assets/earth/{i}.png')).convert_alpha()
            self.frames.append(img)

        self.animation_timer = 0
        self.current_frame = 0 
        self.image = self.frames[self.current_frame]
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.screen_rect.midbottom
        self.image_rect.top = self.image_rect.top + 250

    
    def update(self, dt):
        """Updates the frames"""
        self.animation_timer += 130 * dt
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    def blitme(self):
        """Puts on the screen."""
        self.screen.blit(self.image, self.image_rect)