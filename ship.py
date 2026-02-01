import pygame

class Ship:
    """A class to manage the ship"""
    
    def __init__(self, ai_game):
            """Initialize the ship and set its starting position"""
            self.screen = ai_game.screen
            self.screen_rect = ai_game.screen.get_rect()
            self.settings = ai_game.settings

            # Load the ship image and get its rect.
            self.image = pygame.image.load('assets/player_ship.png')
            self.rect = self.image.get_rect()

            # Start each new ship at the bottom centre of the screen.
            self.rect.midbottom = self.screen_rect.midbottom

            # Store a float for the ship's exact horizontal & vertical position
            self.x = float(self.rect.x)
            self.y = float(self.rect.y)

            # Movement flag: start with a ship that's not moving.
            self.moving_right = False
            self.moving_left = False
            self.moving_up = False
            self.moving_down = False
            self.ship_centred = False

    def update(self, dt):
          """Updates the ship's position based on movement flags"""
          
          # Update the ship's x value, not the rect.
          if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed * dt
          if self.moving_left and self.rect.left > self.screen_rect.left:
                self.x -= self.settings.ship_speed * dt
          
          # Update rect object from self.x

          if self.moving_up and self.rect.top > self.screen_rect.top:
                self.y -= self.settings.ship_speed * dt     
          if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.ship_speed * dt

          self.rect.x = self.x      
          self.rect.y = self.y   
          
          if self.ship_centred:
                self.rect.midbottom = self.screen_rect.midbottom 
                self.ship_centred = False

                self.x = float(self.rect.x)
                self.y = float(self.rect.y)  
            
                self.rect.x = self.x      
                self.rect.y = self.y   
          
    def blitme(self):
          """Draw the ship at its current location"""
          self.screen.blit(self.image, self.rect)
