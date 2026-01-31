import pygame

class Earth:
    """Earth Animation"""

    def __init__(self, ai_game):
        """Initialize Earth animation."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.frames = [
            pygame.image.load('assets/earth/0001.png'),
            pygame.image.load('assets/earth/0002.png'),
            pygame.image.load('assets/earth/0003.png'),
            pygame.image.load('assets/earth/0004.png'),
            pygame.image.load('assets/earth/0005.png'),
            pygame.image.load('assets/earth/0006.png'),
            pygame.image.load('assets/earth/0007.png'),
            pygame.image.load('assets/earth/0008.png'),
            pygame.image.load('assets/earth/0009.png'),
            pygame.image.load('assets/earth/0010.png'),
            pygame.image.load('assets/earth/0011.png'),
            pygame.image.load('assets/earth/0012.png'),
            pygame.image.load('assets/earth/0013.png'),
            pygame.image.load('assets/earth/0014.png'),
            pygame.image.load('assets/earth/0015.png'),
            pygame.image.load('assets/earth/0016.png'),
            pygame.image.load('assets/earth/0017.png'),
            pygame.image.load('assets/earth/0018.png'),
            pygame.image.load('assets/earth/0019.png'),
            pygame.image.load('assets/earth/0020.png'),
            pygame.image.load('assets/earth/0021.png'),
            pygame.image.load('assets/earth/0022.png'),
            pygame.image.load('assets/earth/0023.png'),
            pygame.image.load('assets/earth/0024.png'),
            pygame.image.load('assets/earth/0025.png'),
            pygame.image.load('assets/earth/0026.png'),
            pygame.image.load('assets/earth/0027.png'),
            pygame.image.load('assets/earth/0028.png'),
            pygame.image.load('assets/earth/0029.png'),
            pygame.image.load('assets/earth/0030.png'),
            pygame.image.load('assets/earth/0031.png'),
            pygame.image.load('assets/earth/0032.png'),
            pygame.image.load('assets/earth/0033.png'),
            pygame.image.load('assets/earth/0034.png'),
            pygame.image.load('assets/earth/0035.png'),
            pygame.image.load('assets/earth/0036.png'),
            pygame.image.load('assets/earth/0037.png'),
            pygame.image.load('assets/earth/0038.png'),
            pygame.image.load('assets/earth/0039.png'),
            pygame.image.load('assets/earth/0040.png'),
            pygame.image.load('assets/earth/0041.png'),
            pygame.image.load('assets/earth/0042.png'),
            pygame.image.load('assets/earth/0043.png'),
            pygame.image.load('assets/earth/0044.png'),
            pygame.image.load('assets/earth/0045.png'),
            pygame.image.load('assets/earth/0046.png'),
            pygame.image.load('assets/earth/0047.png'),
            pygame.image.load('assets/earth/0048.png'),
            pygame.image.load('assets/earth/0049.png'),
            pygame.image.load('assets/earth/0050.png'),
            pygame.image.load('assets/earth/0051.png'),
            pygame.image.load('assets/earth/0052.png'),
            pygame.image.load('assets/earth/0053.png'),
            pygame.image.load('assets/earth/0054.png'),
            pygame.image.load('assets/earth/0055.png'),
            pygame.image.load('assets/earth/0056.png'),
            pygame.image.load('assets/earth/0057.png'),
            pygame.image.load('assets/earth/0058.png'),
            pygame.image.load('assets/earth/0059.png'),
            pygame.image.load('assets/earth/0060.png'),
            pygame.image.load('assets/earth/0061.png'),
            pygame.image.load('assets/earth/0062.png'),
            pygame.image.load('assets/earth/0063.png'),
            pygame.image.load('assets/earth/0064.png'),
            pygame.image.load('assets/earth/0065.png'),
            pygame.image.load('assets/earth/0066.png'),
            pygame.image.load('assets/earth/0067.png'),
            pygame.image.load('assets/earth/0068.png'),
            pygame.image.load('assets/earth/0069.png'),
            pygame.image.load('assets/earth/0070.png'),
            pygame.image.load('assets/earth/0071.png'),
            pygame.image.load('assets/earth/0072.png'),
            pygame.image.load('assets/earth/0073.png'),
            pygame.image.load('assets/earth/0074.png'),
            pygame.image.load('assets/earth/0075.png'),
            pygame.image.load('assets/earth/0076.png'),
            pygame.image.load('assets/earth/0077.png'),
            pygame.image.load('assets/earth/0078.png'),
            pygame.image.load('assets/earth/0079.png'),
            pygame.image.load('assets/earth/0080.png'),
            pygame.image.load('assets/earth/0081.png'),
            pygame.image.load('assets/earth/0082.png'),
            pygame.image.load('assets/earth/0083.png'),
            pygame.image.load('assets/earth/0084.png'),
            pygame.image.load('assets/earth/0085.png'),
            pygame.image.load('assets/earth/0086.png'),
            pygame.image.load('assets/earth/0087.png'),
            pygame.image.load('assets/earth/0088.png'),
            pygame.image.load('assets/earth/0089.png'),
            pygame.image.load('assets/earth/0090.png'),
            pygame.image.load('assets/earth/0091.png'),
            pygame.image.load('assets/earth/0092.png'),
            pygame.image.load('assets/earth/0093.png'),
            pygame.image.load('assets/earth/0094.png'),
            pygame.image.load('assets/earth/0095.png'),
            pygame.image.load('assets/earth/0096.png'),
            pygame.image.load('assets/earth/0097.png'),
            pygame.image.load('assets/earth/0098.png'),
            pygame.image.load('assets/earth/0099.png'),
            pygame.image.load('assets/earth/0100.png'),
            pygame.image.load('assets/earth/0101.png'),
            pygame.image.load('assets/earth/0102.png'),
            pygame.image.load('assets/earth/0103.png'),
            pygame.image.load('assets/earth/0104.png'),
            pygame.image.load('assets/earth/0105.png'),
            pygame.image.load('assets/earth/0106.png'),
            pygame.image.load('assets/earth/0107.png'),
            pygame.image.load('assets/earth/0108.png'),
            pygame.image.load('assets/earth/0109.png'),
            pygame.image.load('assets/earth/0110.png'),
            pygame.image.load('assets/earth/0111.png'),
            pygame.image.load('assets/earth/0112.png'),
            pygame.image.load('assets/earth/0113.png'),
            pygame.image.load('assets/earth/0114.png'),
            pygame.image.load('assets/earth/0115.png'),
            pygame.image.load('assets/earth/0116.png'),
            pygame.image.load('assets/earth/0117.png'),
            pygame.image.load('assets/earth/0118.png'),
            pygame.image.load('assets/earth/0119.png'), 
        ]

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