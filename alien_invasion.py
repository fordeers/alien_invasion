from random import randint
import sys

import pygame

from settings import Settings
from bullet import *
from alien import Aliens
from ship import Ship
from star import Star
from spacedrop import SpaceDrop


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_get_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("AlienInvasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rbullets = pygame.sprite.Group()
        self.lbullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.spacedrops = pygame.sprite.Group()

        # self._create_fleet()
        self._create_stars()
        #self._create_drops()

        self.warping = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.dt = self.clock.tick(self.settings.fps) / 1000
            print(self.clock.get_fps())
            self._check_events()
            self.ship.update(self.dt)
            self._update_bullets(self.dt)
            self._update_aliens(self.dt)
            self.stars.update(self.dt)
            self._update_space_drops(self.dt)
            # self._flags_for_spacewarp(self.dt)
            self._update_screen()

    def _update_screen(self):
        """Updates assets on the screen, and flips to the new screen """
        # Redraw colours & assets on the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_colour)
        self.stars.draw(self.screen)
        # for bullet in self.bullets.sprites():
        #     bullet.draw_bullet()
        self._draw_bullets()
        self.aliens.draw(self.screen)
        self._space_drops_draw()
        self.ship.blitme()

        # Make a game instance, run the game.
        pygame.display.flip()
         
    def _quit_game(self): 
        """quits and exits programs"""
        pygame.quit()
        sys.exit()

    def _check_events(self):
        """Watch for keyboard and mouse events."""
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self._quit_game()

                if event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                if event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            # self.warping = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            # self.warping = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
            # self.warping = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_f:
            self.settings._fullscreen_mode()
        elif event.key == pygame.K_ESCAPE:
            self.settings._exit_fullscreen()
            
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            # self.warping = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            # self.warping = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
            # self.warping = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    ############################## SpaceDrops ##############################

    def _space_drops_draw(self):
        """Draws Spacedrops"""
        if self.spacedrops:
            for drop in self.spacedrops.sprites():
                drop.draw_space_drops()

    def _keybased_spacedrops(self, dt):
        """For when you want to bind spacedrops warping effect to keypresses."""
        if self.warping:
            self._update_space_drops(dt)
        else:
            for drops in self.spacedrops.sprites():
                self.spacedrops.remove(drops)
    
    def _update_space_drops(self, dt):
        """Updates Spacedrops"""
        self._delete_space_drops_bottom()
        self._create_drops()
        self.spacedrops.update(dt)

    def _delete_space_drops_bottom(self):
        """Deletes spacedrops"""
        for drops in self.spacedrops.sprites():
            #print(drops)

            if drops.rect.bottom > self.screen_get_rect.bottom:
                self.spacedrops.remove(drops) 

    def _create_drops(self):
        """Create spacedrop"""
        if len(self.spacedrops) <= 1:    
            for _ in range(1):    
                new_drops = SpaceDrop(self)
                self.spacedrops.add(new_drops)

    ############################## Stars ##############################
    
    def _create_stars(self):
        """Twinkling stars are created here"""
        for _ in range(10):
            new_star = Star(self)
            self.stars.add(new_star)

    ############################## Aliens ##############################

    def _update_aliens(self, dt):
        """Update the positions of all aliens in the fleet."""
        self._delete_aliens_screen()
        self._create_fleet(dt)
        self._check_fleet_edges(dt)
        self.aliens.update(dt)
        # print(len(self.aliens))

    def _create_fleet(self, dt):
        """Create the fleet of aliens."""
        if len(self.aliens) == 0:
            # Create an alien and keep adding aliens until there's no room left.
            # Spacing between aliens is one alien width and one alien height.
            alien = Aliens(self)
            alien_width, alien_height = alien.rect.size

            current_x, current_y = alien_width, alien_height
            while current_y < (self.settings.screen_height - 20 * alien_height):
                while current_x < (self.settings.screen_width - 3 * alien_width):
                    self._create_alien(current_x, current_y)
                    current_x += 2 * alien_width
                
                # Finished a row: reset x value, and increment y value.
                current_x = alien_width
                current_y += 2 * alien_height

    def _create_alien(self, current_x, current_y):
        """Create an alien and place it in a row"""
        new_alien = Aliens(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)

    def _delete_aliens_screen(self):

        for aliens in self.aliens.sprites():
            #print(aliens)

            if aliens.rect.bottom > self.screen_get_rect.bottom:
                self.aliens.remove(aliens)

    def _check_fleet_edges(self, dt):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien._check_edges():   
                self._change_fleet_direction(dt)
                break
    
    def _change_fleet_direction(self, dt):
        """Drop the entire fleet and change the fleet's direction."""
        
        for alien in self.aliens.sprites(): ####### WORK ON THIS / FIX THIS /FIGURE IT OUT
            
            alien.rect.y += self.settings.fleet_drop_speed * dt
        
        self.settings.fleet_direction *= -1
        
        # for alien in self.aliens.sprites(): ####### Frame based possible solution to the alien drop down bug glitch
            
        #     alien.rect.y += self.settings.fleet_drop_speed * dt

        #     if self.settings.fleet_direction == 1:
        #         alien.rect.right = self.screen_get_rect.right - 1
        #     else:
        #         alien.rect.left = 1
        
        # self.settings.fleet_direction *= -1
        
    ############################## Bullets ##############################

    def _draw_bullets(self):
        """Draw the bullets"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # for rbullet in self.rbullets.sprites():
        #     rbullet.draw_bullet()
        # for lbullet in self.lbullets.sprites():
        #     lbullet.draw_bullet()
            
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
        if len(self.rbullets) < self.settings.bullets_allowed:
            rnew_bullet = RBullet(self)
            self.rbullets.add(rnew_bullet)
        
        if len(self.lbullets) < self.settings.bullets_allowed:
            lnew_bullet = LBullet(self)
            self.lbullets.add(lnew_bullet)

    def _update_bullets(self, dt):
        """Updates bullets"""
        self.bullets.update(dt)
        self.rbullets.update(dt)
        self.lbullets.update(dt)
        self._bullet_boundary_delete()
        self._bullet_group_collision_delete()

    def _bullet_boundary_delete(self):
        """Delete bullets when reaching screen boundary"""
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        for rbullet in self.rbullets.copy():
                if rbullet.rect.right >= self.screen_get_rect.right:
                    self.rbullets.remove(rbullet)
        for lbullet in self.lbullets.copy():
                if lbullet.rect.left <= 0:
                    self.lbullets.remove(lbullet)
    
    def _bullet_group_collision_delete(self):
        """Handles deletition in collision with other sprite groups"""
        pygame.sprite.groupcollide(self.aliens, self.bullets, True, True) 
        pygame.sprite.groupcollide(self.aliens, self.rbullets, True, True) 
        pygame.sprite.groupcollide(self.aliens, self.lbullets, True, True) 


# Main game loop's instance and calling
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
