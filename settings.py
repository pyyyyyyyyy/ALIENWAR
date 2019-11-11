class Settings():
    def __init__(self):
        #屏幕设置
        self.screen_width=1000
        self.screen_height=700
        self.bg_color=(230,230,230)

        #飞船速度设置
        self.ship_limit=3

        #子弹设置
        self.bullets_allowed=3
        self.attacks_allowed=3
        #攻击设置
        self.attack_width=5
        self.attack_height=10
        self.attack_color=(255,255,255)

        #外星人设置
        self.fleet_drop_speed=10

        #设置游戏难度递增
        self.speedup_scale=1.1
        self.score_scale=1.5

        #选择设置
        self.easy_flag=False
        self.difficult_flag=False

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #容易
        self.ship_speed_factor=2
        self.bullet_speed_factor=5
        self.alien_speed_factor=2
        #设置分数
        self.alien_points=50
        # fleet_direction为1表示右移，-1表示左移
        self.fleet_direction=1

    def difficult_dynamic_settings(self):
        #困难
        self.ship_speed_factor=3
        self.bullet_speed_factor=5
        self.alien_speed_factor=3
        #设置分数
        self.alien_points=50
        # fleet_direction为1表示右移，-1表示左移
        self.fleet_direction=1

    def increase_speed(self):
        #设置速度递增
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        #设置分值递增
        self.alien_points=int(self.score_scale*self.alien_points)

#游戏的主要设置
