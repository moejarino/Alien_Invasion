import sys
from time import sleep  # so we can pause the game when the ship is hit

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """This is the app class"""

    def __init__(self):
        """initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        # Fullscreen setting
        # Create fullscreen window first because we don't know size of the screen
        # Next we set the width and height now that the parameters are known
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # Small window setting
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Create an instance of game stats and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # create button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # I used this to ensure bullets were actually being deleted with the terminal
            # print(len(self.bullets))

    def _check_events(self):
        """keyboard and mouse events watched here"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # This is to allow for continuos movement when key is pressed
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Hide cursor
            pygame.mouse.set_visible(False)

            # Reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining alien and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """responds to key release events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of the old ones"""
        # update position
        self.bullets.update()

        # Get rid of bullets that have disappeared
        # can't remove items from a list or group within a for loop
        # the copy method allows us to modify bullets inside the loop
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_and_alien_collisions()

    def _check_bullet_and_alien_collisions(self):
        # Check for bullets that have hit any aliens
        # The two booleans indicate which disappears after collison
        # In this case we want both to disappear
        #****Change first boolean for testing***
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # any bullet that hits becomes a key in collisions dict
        # loop through this to assure each alien hit gives points
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create fleet
            self.bullets.empty()
            self._create_fleet()
            # Increase the speed after all the aliens have been shot
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """create the fleet of aliens"""
        # create an alien and find the number of aliens in a row
        # The space between each alien ship is the width of an alien ship
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # the (2 * alien_width) accounts for the margin on either side of the screen
        # which is the width of one alien ship
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # we use the available space, floor division (to round down so no remainder)
        # and each alien occupies 2 widths, one for the ship and one for margin
        number_aliens_x = available_space_x // (2 * alien_width)
        # Determine the number of rows of aliens that fit onto the screen
        # available vertical space found by subtracting alien height from top,
        # the ship height from the bottom, and two alien heights from bottom
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (5 * ship_height) - ship_height)
        # an alien occupies 2 ship heights, one for ship and one for margin
        number_rows = available_space_y // (2 * alien_height)
        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create an alien and place it in the row
        alien = Alien(self)
        #.size contains tuple with the width and height of a rect object
        alien_width, alien_height = alien.rect.size
        # this sets the alien ship created to the correct position in the row
        # alien is pushed one width over to account for margin
        # then multiplied by two to account for space an alien takes up
        # then finally multiply by the number in the row
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # one alien height or margin from top plus two alien heights to signify
        # the start of next row, multiplied by the row number
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """response if alien reaches an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treating as if ship got hit
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and change its horizontal direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # multiply by negative one in order to change directions
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left and update sb
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # creat new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """
        Check if the fleet of aliens is at an edge,
        and update position of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom
        self._check_aliens_bottom()

    def _update_screen(self):
        """Update images on the screen, and flip the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # bullets.sprites returns all the bullets that are in the group and for loop iterates
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw score info
        self.sb.show_score()

        # Draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # make game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
