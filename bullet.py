import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self,ai_settings,screen,ship):
        super(Bullet,self).__init__()
        self.screen=screen

        # 创建一个子弹对象
        self.image = pygame.image.load('./images/fire.bmp')
        self.rect = self.image.get_rect()

        #移动至飞船处
        self.rect.centerx=ship.rect.centerx
        self.rect.top=ship.rect.top

        #以小数形式存储子弹纵坐标
        self.y=float(self.rect.y)

        #子弹属性设置
        self.speed_factor=ai_settings.bullet_speed_factor

    def update(self):
        self.y-=self.speed_factor
        self.rect.y=self.y

    def draw_bullet(self):
        self.screen.blit(self.image,self.rect)
