import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self,screen,ai_settings):
        super(Ship,self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        self.image=pygame.image.load('./images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=self.screen.get_rect()
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.moving_right=False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.center=float(self.rect.centerx)
    #飞船的属性

    def update(self):
        if self.moving_right and self.rect.centerx<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.centerx>0:
            self.center-=self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.y>0:
            self.rect.y-=self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.rect.y+= self.ai_settings.ship_speed_factor
        self.rect.centerx=self.center
    #飞船的移动

    def blitme(self):
        self.screen.blit(self.image,self.rect)
    #飞船的创建

    def center_ship(self):
        self.center=self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom