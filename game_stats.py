#game-stats.py
import game_functions as gf

class GameStats():
    """Tracks player stats."""

    def __init__(self, game_settings):
        """Init stats."""
        self.game_settings = game_settings
        self.reset_stats()

        self.high_score = gf.read_in_high_scores()

        self.game_active = False


    def reset_stats(self):
        """Init stats that can change during the game."""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1
