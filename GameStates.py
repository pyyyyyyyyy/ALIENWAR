class Gamestates():
    def __init__(self, ai_settings):
        #初始化统计信息
        self.ai_settings = ai_settings
        self.reset_stats()

        self.game_active = False
        self.high_score = 0       #任何情况下不得重置
        self.level = 1

    def reset_stats(self):
        #初始化游戏中各种信息
        self.ships_left = self.ai_settings.ship_limit  #飞船数
        self.score = 0
        self.level = 1
