import pygame.font


class Button():
    def __init__(self,ai_settings,screen,msg,left_path):
        self.screen=screen
        self.screen_rect=screen.get_rect()

        #设置按钮尺寸和属性
        self.width,self.height=200,70
        self.button_color=(230,230,250)
        self.text_color=(238,99,99)
        self.font=pygame.font.SysFont('幼圆',48)
        #使按钮居中
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center
        self.rect.left=left_path

        self.prep_msg(msg)

    def prep_msg(self,msg):
        #渲染
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

