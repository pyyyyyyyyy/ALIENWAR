import pygame

class Enemy():
    def __init__(self,screen):
        self.screen=screen
        self.screen_rect=self.screen.get_rect()

        self.image=pygame.image.load('./images/enemy.bmp')
        self.rect=self.image.get_rect()

        self.rect.x=450
        self.rect.top=20

    def blitme(self):
        self.screen.blit(self.image,self.rect)