#ship.py
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    ship_location = 'images/astronaut.bmp'

    def __init__(self, game_settings, screen):
        """Init the ship and set its starting position."""
        super(Ship,self).__init__()
        self.screen = screen

        self.game_settings = game_settings
        self.image = pygame.image.load(Ship.ship_location)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        #Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
