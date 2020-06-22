class Settings:
    """A class to store all the settings for the game"""

    def __init__(self):
        """Initialize the games settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.25

        # Alien point value scaleup speed
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that are changings"""
        self.ship_speed = 1.5
        self.bullet_speed = 7.0
        self.alien_speed = 1.0

        # 1 is right, -1 left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point value"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points) **check to ensure alien point values were increaing
