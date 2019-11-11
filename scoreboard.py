import pygame.font
from pygame.sprite import Group
from ship import Ship
from bullet import Bullet
from enemy import  Enemy

class Scoreboard:
    def __init__(self, ai_settings, screen, states,bullets,ship):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.states = states
        self.ship=ship

        #设置字体
        self.board_color=(255,228,225)
        self.text_color = (139,137,137)
        self.font = pygame.font.SysFont('幼圆',40)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_bulletss(bullets)

    def prep_score(self):
        #渲染分数
        rounded_score = int(round(self.states.score,-1))       #圆整
        score_str ='分数:'+'{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,self.board_color )
        #置于屏幕左上方
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right-40
        self.score_rect.top = 20

    def prep_high_score(self):
        #渲染最高分
        high_score = int(round(self.states.high_score, -1))  # 圆整
        high_score_str = '最高分:'+'{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.board_color)
        #置于屏幕上方
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right-40
        self.high_score_rect.top = 70


    def prep_level(self):
        #渲染
        self.level = self.states.level
        self.level_str= '等级:'+ str(self.level)
        self.level_image = self.font.render(self.level_str, True, self.text_color,self.board_color)

        #位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = 20
        self.level_rect.right =150


    def prep_ships(self):
        #创建编组
        self.ships=Group()
        #创建生命图标
        for ship_number in range(self.states.ships_left):
            ship=Ship(self.screen,self.ai_settings)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=self.screen_rect.bottom-50
            self.ships.add(ship)

    def prep_bulletss(self,bullets):
        self.bulletss=Group()
        bullet_numbers=self.ai_settings.bullets_allowed-len(bullets)
        for bullet_number in range(bullet_numbers):
            bullet=Bullet(self.ai_settings,self.screen,self.ship)
            bullet.rect.y=self.screen_rect.bottom-70
            bullet.rect.x=self.screen_rect.right-200+bullet_number*(bullet.rect.width/2)
            self.bulletss.add(bullet)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)

        self.ships.draw(self.screen)
        self.bulletss.draw(self.screen)

