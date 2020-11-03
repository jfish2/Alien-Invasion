#launcher.py
import pygame
from pygame.sprite import Sprite

class Launcher(Sprite):
    """A class to manage launchers fired from the ship."""

    def __init__(self, game_settings, screen, ship):
        """Create a launcher object at the ship's current position."""
        super(Launcher, self).__init__()
        self.screen = screen

        #Create a launcher rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0,0, game_settings.launcher_width, game_settings.launcher_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store launcher's position as a decimal value
        self.y = float(self.rect.y)

        self.color = game_settings.launcher_color
        self.speed_factor = game_settings.launcher_speed_factor


    def update(self):
        """Move the launcher up the screen by updating the decimal y position of the launcher."""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_launcher(self):
        """Draw the launcher to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
