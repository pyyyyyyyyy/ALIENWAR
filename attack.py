import pygame
from pygame.sprite import Sprite


class Attack(Sprite):
    def __init__(self,enemy,screen,ai_settings):
        super(Attack, self).__init__()
        self.screen=screen

        #攻击子弹发射位置
        self.rect=pygame.Rect(0,0,ai_settings.attack_width,ai_settings.attack_height)
        self.rect.centerx=enemy.rect.centerx
        self.rect.top=enemy.rect.bottom
        #坐标
        self.rect_y =float(self.rect.y)
        #颜色
        self.color=ai_settings.attack_color
        self.speed_factor=ai_settings.bullet_speed_factor

    def update(self):
        self.rect_y+=self.speed_factor
        self.rect.y=self.rect_y

    def draw_attack(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
