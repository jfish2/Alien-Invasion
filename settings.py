#settings.py

class Settings():
    """A class to store all settings for the game. Modifiable to some extene"""

    def __init__(self):
        """Init the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,255,255)
        self.ship_limit = 3

        #Launcher settings
        self.launcher_width = 3
        self.launcher_height = 15
        self.launcher_color = 60,60,60
        self.launchers_allowed = 3


        #Alien settings
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10



        #How quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        #scoring
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """Init the settings that auto update through game."""
        self.ship_speed_factor = 1
        self.launcher_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet direction of 1 represents right dir; -1 represents left direction
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.launcher_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
