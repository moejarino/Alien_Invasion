import pygame

from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""

    # ai_game is instance of alien invasion class
    def __init__(self, ai_game):
        """initialize ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # centering a new ship at the bottom
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """update position based on the movement's flag"""
        # update the ships value not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update the rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """draw the ship at current location for refresh"""
        self.screen.blit(self.image, self.rect)
