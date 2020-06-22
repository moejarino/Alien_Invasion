class GameStats:
    """Track ingame statistics for game"""

    def __init__(self, ai_game):
        """Initialize statistic"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        # Highscore never reset (why it's in __init__)
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
