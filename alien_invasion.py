import sys
from time import sleep
from random import choice, random, uniform

import pygame

from settings import Settings
from bullet import *
from alien import Alien
from ship import Ship
from star import Star
from spacedrop import SpaceDrop
from game_stats import GameStats
from button import Button
from scoreboard_and_levels import ScoreboardAndLevels
from earth import Earth
from player_lives import PlayerLives 


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

        self.stats = GameStats(self)
        self.testbutton = Button(self, 'testbutton')
        self.sb = ScoreboardAndLevels(self)
        self.earth = Earth(self)
        self.ship = Ship(self)
        self.hearts = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.rbullets = pygame.sprite.Group()
        self.lbullets = pygame.sprite.Group()
        self.trbullets = pygame.sprite.Group()
        self.tlbullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.spacedrops = pygame.sprite.Group()

        # Game Buttons instances
        self.play_button = Button(self, "Play")
        self.start_button = Button(self, "Start")
        self.main_level_button = Button(self, "Levels")
        self.leaderboard_button = Button(self, "Leaderboard")
        self.settings_button = Button(self, "Settings")
        self.quit_button = Button(self, "Quit")
        self.work_in_progress = Button(self, "Work In Progress...")
        self.level_button0 = Button(self, "0")
        self.level_button1 = Button(self, "1")
        self.level_button2 = Button(self, "2")
        self.level_button3 = Button(self, "3")
        self.level_button4 = Button(self, "4")
        self.level_button5 = Button(self, "5")

        self._create_stars()
        #self._create_drops()

    ############################## Game Flags ##############################
    
        # Assorted game features
        self.fullscreen = False
        self.warping = False
        self.side_bullets = False
        self.double_bullets = False
        # self.aln_bullets_fire = True
        
        # Start Alien Invasion in an inactive state.
        self.game_active = False

        self.speed_increase = False # Checks true if aliens dont die from border delete 
                                    # and ship to alien collision delete

        # Remove Game button flags to prevent overlapping.
        self.remove_playbutton = False
        
           # Main menu button flags
        self.remove_main_menu_buttons = True
               
               # Under main menu button flags
        self.remove_levelbuttons = True
        self.remove_work_in_progress_button = True
        self.remove_display_top_score = True

        # Flags for making sure unpause button cannot be abused.
        self.escape_button_pause = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.dt = self.clock.tick(self.settings.fps) / 1000
            if self.dt > 0.1: 
                self.dt = 1/60.0
            # print(self.clock.get_fps())
            self._check_events()
            
            if self.game_active:
                pygame.mouse.set_visible(True)    
                self.ship.update(self.dt)
                self._update_bullets(self.dt)
                self._update_aliens(self.dt)
                self.stars.update(self.dt)
                self._update_space_drops(self.dt)
                self.earth.update(self.dt)
                self._create_hearts()
                # _keybased_spacedrops()
            
            if not self.game_active:
                pygame.mouse.set_visible(True)
            
            self._update_screen()

    def _update_screen(self):
        """Updates assets on the screen, and flips to the new screen """
        # Redraw colours & assets on the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_colour)
        self.stars.draw(self.screen)
        self.earth.blitme()
        self.sb.show_score()
        self.hearts.draw(self.screen)
        self._draw_bullets()
        self.aliens.draw(self.screen)
        self._space_drops_draw()
        self.ship.blitme()
        # print(len(self.aliens))
        # print(self.settings.alien_speed)
         # print(self.settings.alien_points)
        # print(self.stats.level)
        # print(len(self.hearts))
        # print(len(self.alien_bullets))


        if not self.game_active and not self.remove_playbutton:
            self.play_button.draw_button()

        elif not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
            self._draw_main_menu_buttons()
        
        elif not self.game_active and self.remove_playbutton and self.remove_main_menu_buttons and not self.remove_levelbuttons:
            self._draw_level_buttons()
    
        elif not self.game_active and self.remove_playbutton and self.remove_main_menu_buttons and not self.remove_work_in_progress_button:
            self.work_in_progress.draw_button()
        
        elif not self.game_active and self.remove_playbutton and self.remove_main_menu_buttons and not self.remove_display_top_score:
            self.sb.display_highest_score()
            self.sb.show_top_score()

        # Make a game instance, run the game.
        pygame.display.flip()
         
    def _quit_game(self): 
        """quits and exits programs"""
        self.sb.record_highest_score()
        pygame.quit()
        sys.exit()

    #############################################################################    
    #############################################################################
    ############################## Key press events #############################
    #############################################################################
    #############################################################################

    def _check_events(self):
        """Watch for keyboard and mouse events."""
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self._quit_game()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._mouse_buttons_collisions (mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            # self.warping = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            # self.warping = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
            # self.warping = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_q:
            self._quit_game()
        # elif event.key == pygame.K_p:
        #     self._p_for_play()
        elif event.key ==pygame.K_r: # Reset button
            if self.game_active:    
                self._master_game_reset()
        elif event.key == pygame.K_d:
            if not self.double_bullets:
                self.double_bullets = True
            elif self.double_bullets:
                self.double_bullets = False
        elif event.key == pygame.K_s:
            if not self.side_bullets:
                self.side_bullets = True
            elif self.side_bullets:
                self.side_bullets = False
        elif event.key == pygame.K_f:
            if not self.fullscreen:
                self.fullscreen = True
                self.settings._fullscreen_mode()
            elif self.fullscreen:
                self.fullscreen = False
                self.settings._exit_fullscreen()
        elif event.key == pygame.K_ESCAPE:
            self._escape_button_conditions()
           
                # elif not self.game_active:
                #     self.game_active = True
        # elif event.key == pygame.K_0:
        #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #         self.level_zero_stuff()
        # # elif event.key == pygame.K_0:
        # #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        # #         self.level_zero_stuff()       REFERENCE EXMAPLE OF THE OLD CODE BEFORE MODIFIED.
        # elif event.key == pygame.K_1:
        #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #         self.level_one_stuff()
        # elif event.key == pygame.K_2:
        #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #         self.level_two_stuff()
        # elif event.key == pygame.K_3:
        #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #         self.level_three_stuff()
        # elif event.key == pygame.K_4:
        #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #         self.level_four_stuff()
        # elif event.key == pygame.K_5:
        #     if not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #         self.level_five_stuff()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            # self.warping = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            # self.warping = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
            # self.warping = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    #############################################################################
    #############################################################################
    ############################## Button related stuff #########################
    #############################################################################
    #############################################################################

    def _escape_button_conditions(self):
        """Manages conditions for return/back navigating the buttons/main menu of the game"""
        if self.escape_button_pause:
            
            # running game -> play (pause)
            if self.game_active: 
                self.game_active = False
                self.remove_playbutton = False
                self.remove_main_menu_buttons = True
                self.remove_levelbuttons = True
                self.remove_work_in_progress_button = True
                self.remove_display_top_score = True
            
            # play -> game
            elif not self.game_active and not self.remove_playbutton and self.remove_main_menu_buttons: 
                self.game_active = True
                self.remove_playbutton = True
                self.remove_main_menu_buttons = True
                self.remove_levelbuttons = True
                self.remove_work_in_progress_button = True
                self.remove_display_top_score = True
            
            # Main menu -> play
            elif not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
                self.remove_playbutton = False
                self.remove_main_menu_buttons = True
                self.remove_levelbuttons = True
                self.remove_work_in_progress_button = True
                self.remove_display_top_score = True
            
            # Levels -> Main menu
            elif not self.game_active and self.remove_playbutton and self.remove_main_menu_buttons and not self.remove_levelbuttons:
                self.remove_main_menu_buttons = False
                self.remove_levelbuttons = True
                self.remove_work_in_progress_button = True
                self.remove_display_top_score = True
            
            # Leaderboard -> Main menu
            elif not self.game_active and self.remove_playbutton and self.remove_main_menu_buttons and not self.remove_display_top_score:
                self.remove_main_menu_buttons = False
                self.remove_levelbuttons = True
                self.remove_work_in_progress_button = True
                self.remove_display_top_score = True
            
            # Settings -> Main menu
            elif not self.game_active and self.remove_playbutton and self.remove_main_menu_buttons and not self.remove_work_in_progress_button:
                self.remove_main_menu_buttons = False
                self.remove_levelbuttons = True
                self.remove_work_in_progress_button = True
                self.remove_display_top_score = True
            
    def _p_for_play(self):
        """Press "P" to play"""
        # If needed, rewrite this code. keybinded button presses temporarily removed for now.

    def _draw_main_menu_buttons(self):
        """Draws the game's main menu buttons."""
        self.start_button.rect.center = self.screen_get_rect.center
        self.start_button.rect.top = self.screen_get_rect.top + 250 
        self.start_button.draw_button()
        self.main_level_button.rect.top = self.start_button.rect.bottom + 15            
        self.main_level_button.draw_button()
        self.leaderboard_button.rect.top = self.main_level_button.rect.bottom + 15
        self.leaderboard_button.draw_button()
        self.settings_button.rect.top = self.leaderboard_button.rect.bottom + 15
        self.settings_button.draw_button()
        self.quit_button.rect.top = self.settings_button.rect.bottom + 15
        self.quit_button.draw_button()

    def _draw_level_buttons(self):
        """Draw level buttons neatly"""
        self.level_button0.msg_image_rect.centerx = self.screen_get_rect.centerx - self.level_button0.msg_image_rect.height
        self.level_button0.msg_image_rect.centery = self.screen_get_rect.centery - 110
        self.level_button0.draw_button()
        self.level_button1.msg_image_rect.centerx = self.level_button0.msg_image_rect.centerx + self.level_button0.msg_image_rect.height + 20
        self.level_button1.msg_image_rect.centery = self.level_button0.msg_image_rect.centery
        self.level_button1.draw_button()
        self.level_button2.msg_image_rect.centerx = self.level_button0.msg_image_rect.centerx 
        self.level_button2.msg_image_rect.centery = self.level_button0.msg_image_rect.centery + self.level_button0.msg_image_rect.height + 20
        self.level_button2.draw_button()
        self.level_button3.msg_image_rect.centerx = self.level_button1.msg_image_rect.centerx 
        self.level_button3.msg_image_rect.centery = self.level_button1.msg_image_rect.centery + self.level_button0.msg_image_rect.height + 20
        self.level_button3.draw_button()
        self.level_button4.msg_image_rect.centerx = self.level_button2.msg_image_rect.centerx 
        self.level_button4.msg_image_rect.centery = self.level_button2.msg_image_rect.centery + self.level_button0.msg_image_rect.height + 20
        self.level_button4.draw_button()
        self.level_button5.msg_image_rect.centerx = self.level_button3.msg_image_rect.centerx 
        self.level_button5.msg_image_rect.centery = self.level_button3.msg_image_rect.centery + self.level_button0.msg_image_rect.height + 20
        self.level_button5.draw_button()

    def _mouse_buttons_collisions (self, mouse_pos):
        """Start a new game when the player clicks Play."""
        # print('test')
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active and not self.remove_playbutton:
            self.remove_playbutton = True
            self.remove_main_menu_buttons = False
            print('testplay')
        
        elif self.start_button.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
            self.remove_main_menu_buttons = True
            self.level_zero_stuff()
        
        elif self.main_level_button.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
            self.remove_main_menu_buttons = True
            self.remove_levelbuttons = False
        
        elif self.leaderboard_button.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
            self.remove_main_menu_buttons = True
            self.remove_display_top_score = False
        
        elif self.settings_button.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
            self.remove_main_menu_buttons = True
            self.remove_work_in_progress_button = False
        
        elif self.quit_button.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_playbutton and not self.remove_main_menu_buttons:
            self._quit_game()

        # elif self.level_button0.rect.collidepoint(mouse_pos) and not self.game_active and not self.remove_levelbuttons and self.remove_playbutton:
        #     self.level_zero_stuff()        REFERENCE EXMAPLE OF THE OLD CODE BEFORE MODIFIED.
        
        elif self.level_button0.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_main_menu_buttons:
            self.level_zero_stuff()
        
        elif self.level_button1.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_main_menu_buttons:
            self.level_one_stuff()
            
        elif self.level_button2.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_main_menu_buttons:
            self.level_two_stuff()
            
        elif self.level_button3.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_main_menu_buttons:
            self.level_three_stuff()

        elif self.level_button4.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_main_menu_buttons:
            self.level_four_stuff()
        
        elif self.level_button5.rect.collidepoint(mouse_pos) and not self.game_active and self.remove_main_menu_buttons:
            self.level_five_stuff()
       
    def level_zero_stuff(self):
        """Level 0 stuff"""
        self._master_game_reset()
        self.sb.level_display()
        self.sb.check_highest_level()
        self.game_active = True
        # print('TEST0')

    def level_one_stuff(self):
        """Level 1 stuff"""
        self._master_game_reset()
        self._level_update_and_speed_increase()
        self.game_active = True
        # print('TEST1')
    
    def level_two_stuff(self):
        """Level 2stuff"""
        self._master_game_reset()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self.game_active = True
        # print('TEST2')
    
    def level_three_stuff(self):
        """Level 3 stuff"""
        self._master_game_reset()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        
        self.game_active = True
        # print('TEST3')
    
    def level_four_stuff(self):
        """Level 4 stuff"""
        self._master_game_reset()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        
        self.game_active = True
        # print('TEST4')
    
    def level_five_stuff(self):
        """Level 5 stuff"""
        self._master_game_reset()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        self._level_update_and_speed_increase()
        
        self.game_active = True
        # print('TEST5')

    #############################################################################    
    #############################################################################
    ############################## Game stats modifiers #########################
    #############################################################################
    #############################################################################

    def _level_update_and_speed_increase(self):
        """Updates current level based on speed increases"""
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.level_display()
        self.sb.check_highest_level()

    def _speed_and_difficulty_increase(self):
        """Checks & Manages conditions for speed and difficulty triggers
        throughout the game thats player influenced."""
        if not self.aliens and self.speed_increase:
            self._level_update_and_speed_increase()
    
    def _master_game_reset(self):
        """Resets game sprites and stats."""
        self.escape_button_pause = True
        self.speed_increase = False
        self._reset_game_sprites()
        self.settings.initialize_dynamic_settings()
        self.sb.check_highest_level()
        self.sb.check_high_score()
        self.stats.reset_stats()
        self.sb.prep_score()
    
    def _no_more_lives_left_pause(self):
        """For when the needs the pause after no more lives left game over"""
        self.game_active = False
        self.escape_button_pause = False
        self.settings.initialize_dynamic_settings()

    #############################################################################    
    #############################################################################
    ############################## Ship/Player ##################################
    #############################################################################
    #############################################################################

    def _ships_and_hearts_link(self):
        """This links ships left and hearts by updating 
        based on current game status"""
        self.stats.ships_left -= 1
        self._delete_hearts()

    def _create_hearts(self):
        """Create and displays all the hearts""" 
        # This code is inspired from _create_fleet()
        # Had a hard time fully understanding and modifying this code
        # But in the end i got it to work by altering the marked lines below *
        # And putting them in their respective spots
        if len(self.hearts) == 0:
            heart = PlayerLives(self)
            heart_width, heart_height = heart.rect.size

            current_x, current_y = heart_width, heart_height
            current_y = self.sb.high_score_rect.y # *this
            while current_y < (self.sb.highest_level_rect.y):
                current_x = self.screen_get_rect.left + 18 # *this
                while current_x < (self.sb.high_score_rect.x - 2 * heart_width):
                    self._create_heart(current_x, current_y)
                    current_x += 1 * heart_width
                
                # Finished a row: reset x value, and increment y value.
                current_x = heart_width
                current_y += 1 * heart_height

    def _create_heart(self, current_x, current_y):
        """Create an heart and place it in a row"""
        if len(self.hearts) < self.stats.ships_left:
            new_heart = PlayerLives(self)
            new_heart.x = current_x
            new_heart.rect.x = current_x
            new_heart.rect.y = current_y
            self.hearts.add(new_heart)
        
    def _delete_hearts(self):
        """Delete hearts based on conditions"""
        for heart in self.hearts.sprites():
            self.hearts.remove(heart)

    def _ship_hit(self):
        """Respond to the ship being hit by an Alien"""
        if self.stats.ships_left > 0:    
            # Decrement ships_left
            self._ships_and_hearts_link()
            self._reset_game_sprites()
        
        else:
            self._no_more_lives_left_pause()
    
    def _reset_game_sprites(self):
        """reset sprites on screen"""
        self.remove_playbutton = False
        self.remove_levelbuttons = True
        
        # Get rid of any remaining bullets and aliens.
        self._empty_all_bullets()
        self.aliens.empty()

        # Center the ship.
        self.ship.ship_centred = True

        # Pause.
        sleep(0.5)

    #############################################################################    
    #############################################################################
    ############################## Spacedrops ###################################
    #############################################################################
    #############################################################################

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

    #############################################################################    
    #############################################################################
    ############################## Stars #######################################
    #############################################################################
    #############################################################################
    
    def _create_stars(self):
        """Twinkling stars are created here"""
        for _ in range(10):
            new_star = Star(self)
            self.stars.add(new_star)

    #############################################################################    
    #############################################################################
    ####################################### Aliens ##############################
    #############################################################################
    #############################################################################

    def _update_aliens(self, dt):
        """Update the positions of all aliens in the fleet."""
        self._delete_aliens_screen()
        self._speed_and_difficulty_increase()
        self._create_fleet()
        self._check_fleet_edges(dt)
        self._alien_bullets_fire()
        self._ship_to_alien_collision()
        self.aliens.update(dt)

    def _alien_bullets_fire(self):
        """Manages conditions for alien bullets firing"""
        # self.fire_time_speed = uniform(0, 0.1)
        # self.ab_fire_timer = 0
        # self.ab_fire_timer += dt

        # if self.ab_fire_timer == self.fire_time_speed:
        #     self.ab_fire_timer = 0
        if len(self.alien_bullets) < self.settings.enemy_bullets_allowed:
            alien_bullet = AlienBullet(self)
            alien = choice(self.aliens.sprites())
            alien_bullet.rect.midbottom = alien.rect.midbottom
            alien_bullet.y = float(alien_bullet.rect.y) # this bug has finally been fixed where the bullets 
                                                        # dont spawn from aliens but the very top instead
                                                        # the problem was the init of the class is inherently setting the y rect to default which is 0 
                                                        # thats why it spawn up top of the screen which is 0 y axis
            self.alien_bullets.add(alien_bullet)

    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        if len(self.aliens) == 0:
            self._empty_all_bullets()
            # Create an alien and keep adding aliens until there's no room left.
            # Spacing between aliens is one alien width and one alien height.
            alien = Alien(self)
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
        if len(self.aliens) != self.settings.alien_fleet_size:
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            new_alien.rect.y = current_y
            self.aliens.add(new_alien)

    def _delete_aliens_screen(self):

        for aliens in self.aliens.sprites():
            #print(aliens)

            if aliens.rect.bottom > self.screen_get_rect.bottom:
                self.speed_increase = False
                self.aliens.remove(aliens)

                if not self.aliens:

                    if self.stats.ships_left > 0:
                        self._ships_and_hearts_link()
                    
                    else:
                        self._no_more_lives_left_pause()

            else:
                self.speed_increase = True
               
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
        
    def _ship_to_alien_collision(self):
        """Detects ship to alien collision"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.speed_increase = False
            self._ship_hit()
        else:
            self.speed_increase = True
            
    #############################################################################    
    #############################################################################
    ############################## Bullets ######################################
    #############################################################################
    #############################################################################

    def _draw_bullets(self):
        """Draw the bullets"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for rbullet in self.rbullets.sprites():
            rbullet.draw_bullet()
        for lbullet in self.lbullets.sprites():
            lbullet.draw_bullet()
        for trbullet in self.trbullets.sprites():
            trbullet.draw_bullet()
        for tlbullet in self.tlbullets.sprites():
            tlbullet.draw_bullet()
        for self.alien_bullet in self.alien_bullets.sprites():
            self.alien_bullet.draw_bullet()
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
        if self.side_bullets:
            if len(self.rbullets) < self.settings.bullets_allowed:
                rnew_bullet = RBullet(self)
                self.rbullets.add(rnew_bullet)
            
            if len(self.lbullets) < self.settings.bullets_allowed:
                lnew_bullet = LBullet(self)
                self.lbullets.add(lnew_bullet)
        
        if self.double_bullets:
            if len(self.trbullets) < self.settings.bullets_allowed:
                trnew_bullet = TRBullet(self)
                self.trbullets.add(trnew_bullet)
            
            if len(self.tlbullets) < self.settings.bullets_allowed:
                tlnew_bullet = TLBullet(self)
                self.tlbullets.add(tlnew_bullet)
    
    def _update_bullets(self, dt):
        """Updates bullets"""
        self.bullets.update(dt)
        self.rbullets.update(dt)
        self.lbullets.update(dt)
        self.trbullets.update(dt)
        self.tlbullets.update(dt)
        self.alien_bullets.update(dt)
        self._bullet_boundary_delete()
        self.bullet_score_updater()
        self._alien_bullets_updater()

    def _empty_all_bullets(self):
        """Empties all bullet sprites"""
        self.bullets.empty()
        self.rbullets.empty()
        self.lbullets.empty()
        self.trbullets.empty()
        self.tlbullets.empty()
        self.alien_bullets.empty()

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
        for trbullet in self.trbullets.copy():
                if trbullet.rect.bottom <= 0:
                    self.trbullets.remove(trbullet)
        for tlbullet in self.tlbullets.copy():
                if tlbullet.rect.bottom <= 0:
                    self.tlbullets.remove(tlbullet)
        for alien_bullet in self.alien_bullets.copy():
                if alien_bullet.rect.top >= self.screen_get_rect.bottom:
                    self.alien_bullets.remove(alien_bullet)
    
    def _bullet_group_collision_delete(self):
        """Handles deletition in collision with other sprite groups"""
        if pygame.sprite.groupcollide(self.aliens, self.bullets, True, True):
            return True
        if pygame.sprite.groupcollide(self.aliens, self.rbullets, True, True):
            return True
        if pygame.sprite.groupcollide(self.aliens, self.lbullets, True, True): 
            return True
        if pygame.sprite.groupcollide(self.aliens, self.trbullets, True, True): 
            return True
        if pygame.sprite.groupcollide(self.aliens, self.tlbullets, True, True): 
            return True
            
    
    def bullet_score_updater(self):
         if self._bullet_group_collision_delete():
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

    def _alien_bullets_updater(self):
        """Manages conditions when enemy bullet hits player"""
        if self.stats.ships_left > 0 and self._ship_bullet_collision():
            self._ships_and_hearts_link()
            self.ship.ship_hit =  True############# This is where you're currently working
        
        elif self.stats.ships_left == 0 and self._ship_bullet_collision():
            self._no_more_lives_left_pause() 

    def _ship_bullet_collision(self):
        """checks enemy bullets hitting player ship"""
        if pygame.sprite.spritecollide(self.ship, self.alien_bullets, True):
            return True

            


# Main game loop's instance and calling
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
