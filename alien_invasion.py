import pygame
from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from GameStates import Gamestates
from button import Button
from scoreboard import Scoreboard
from enemy import Enemy

def run_game():
    #初始化
    pygame.init()
    pygame.mixer.init()
    #创建实例
    ai_settings=Settings()
    states=Gamestates(ai_settings)
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ship = Ship(screen, ai_settings)
    enemy=Enemy(screen)
    #创建子弹，外星人编组
    bullets = Group()
    aliens = Group()
    attacks=Group()
    score=Scoreboard(ai_settings,screen,states,bullets,ship)
    #设置背景
    background = pygame.image.load('./images/space.bmp')
    #设置背景音乐
    pygame.mixer.music.load('./images/space.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(4.0)
    #创建按钮
    play_button = Button(ai_settings, screen, u'入门',200)
    difficult_button = Button(ai_settings, screen, u'困难',600)
    #窗口设置
    pygame.display.set_caption('Alien Invasion')
    gf.create_fleet(ai_settings,screen,states,aliens)

    while True:
        screen.blit(background, (0, 0))
        gf.check_events(ai_settings,screen,ship,bullets,states,play_button,aliens,score,difficult_button,attacks,enemy)
        if states.game_active:
            ship.update()
            gf.update_aliens(aliens,ai_settings,ship,states,screen,bullets,score,attacks)
            gf.update_bullets(bullets,ai_settings,screen,aliens,states,score,ship)
            gf.update_attacks(attacks, ai_settings, screen, aliens, states, score, ship, bullets)
        gf.update_screen(attacks, screen,ship,bullets,aliens,states,play_button,score,difficult_button,enemy,ai_settings)
        pygame.display.update()
    #游戏的主循环


run_game()

