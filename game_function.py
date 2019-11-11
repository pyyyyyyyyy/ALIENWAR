import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from attack import Attack

def check_events(ai_settings,screen,ship,bullets,states,play_button,aliens,score,difficult_button,attacks,enemy):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_event(event, ai_settings,screen,ship,bullets,score,attacks,enemy)
        elif event.type==pygame.KEYUP:
            check_keyup_event(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(states,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,score,attacks)
            check_difficult_button(states, difficult_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, score,attacks)
    #检测事件，控制游戏


def check_keydown_event(event,ai_settings,screen,ship,bullets,score,attacks,enemy):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key==pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship,score)
        if ai_settings.difficult_flag:
            fire_attacks(attacks,screen,enemy,ai_settings)
    elif event.key==pygame.K_q:
        sys.exit()


def check_keyup_event(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_edges(ai_settings,aliens):
    #检查是否到达边界
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def update_screen(attacks,screen,ship,bullets,aliens,states,play_button,score,difficult_button,enemy,ai_settings):
    #遍历编组中所有精灵，绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        score.prep_bulletss(bullets)
    #绘制敌军子弹
    if ai_settings.difficult_flag:
        for attack in attacks.sprites():
            attack.draw_attack()
    ship.blitme()
    if ai_settings.difficult_flag:
        enemy.blitme()
    aliens.draw(screen)
    score.show_score()      #在绘制play前 绘制分数栏
    if not states.game_active:
        play_button.draw_button()
        difficult_button.draw_button()


def update_bullets(bullets,ai_settings,screen,aliens,states,score,ship):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            score.prep_bulletss(bullets)
    check_bullet_alien_collision(bullets, aliens, ai_settings, screen,states,score,ship)

def update_attacks(attacks,ai_settings,screen,aliens,states,score,ship,bullets):
    if ai_settings.difficult_flag:
        attacks.update()
        #删除已出界的子弹
        for attack in attacks.copy():
            if attack.rect.bottom>= ai_settings.screen_height:
                attacks.remove(attack)
        check_attacks_ship_collision(attacks, aliens, ai_settings, screen, states, ship, bullets, score)


def check_attacks_ship_collision(attacks,aliens,ai_settings,screen,states,ship,bullets,score):
    #检查敌军是否攻击到我方
    #遍历攻击子弹编组
    for attack in attacks.sprites():
        if pygame.Rect.colliderect(attack.rect,ship.rect):
            states.score -= 100
            score.prep_score()
            ship_hit(ai_settings,states,screen,aliens,bullets,ship,score,attacks)


def check_bullet_alien_collision(bullets,aliens,ai_settings,screen,states,score,ship):
    #检查是否碰撞,并删除
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    #更新分数
    if collisions:
        #遍历每个碰撞的子弹消灭的外星人（字典），确保分数值的正确
        for aliens in collisions.values():
            states.score+=ai_settings.alien_points*len(aliens)
            score.prep_score()
        check_high_score(states, score)
    #外星人消灭完毕后，创建新的一波外星人
    if len(aliens) == 0:
        bullets.empty()     #清空子弹
        score.prep_bulletss(bullets)
        ai_settings.increase_speed()        #增加游戏难度
        states.level+=1     #更新等级
        score.prep_level()

        create_fleet(ai_settings,screen,states,aliens)


def update_aliens(aliens,ai_settings,ship,states,screen,bullets,score,attacks):
    #检查是否到达边界，并更新外星人位置
    check_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,states,screen,aliens,bullets,ship,score,attacks)
    check_aliens_bottome(ai_settings, screen, bullets, aliens, states, ship,score,attacks)


def fire_bullet(bullets,ai_settings,screen,ship,score):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        score.prep_bulletss(bullets)
    # 创建新子弹，并加入到编组中


def fire_attacks(attacks,screen,enemy,ai_settings):
    if len(attacks)<ai_settings.attacks_allowed:
         new_attack = Attack(enemy,screen,ai_settings)
         attacks.add(new_attack)


def create_fleet(ai_settings,screen,states,aliens):
    #创建外星人样例
    alien = Alien(ai_settings, screen)
    number_alien_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(states)

    #按行按列创建外星人
    #嵌套循环
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(alien_number, aliens, screen, ai_settings,row_number)


def change_fleet_direction(ai_settings,aliens):
    #到达边界，下落并更改方向
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1


def get_number_aliens_x(ai_settings,alien_width):
    # 计算每行外星人个数
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_number_rows(states):
    #计算可容纳外星人行数
    if states.level<=4:
        number_rows=states.level
    else:
        number_rows=4
    return number_rows


def create_alien(alien_number,aliens,screen,ai_settings,row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width+ 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=2*alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)


def ship_hit(ai_settings,states,screen,aliens,bullets,ship,score,attacks):
    #飞船被撞时做出响应
    #飞船数-1
    states.ships_left-=1
    if states.ships_left>0:
        #清空飞船和外星人
        attacks.empty()
        aliens.empty()
        bullets.empty()
        score.prep_bulletss(bullets)
        score.prep_ships()
        #重新创建外星人
        create_fleet(ai_settings,screen,states,aliens)
        ship.center_ship()      #将新飞船放到中间
        #休眠五秒
        sleep(0.5)
    else:
        states.game_active=False #游戏终止
        ai_settings.easy_flag = False
        ai_settings.difficult_flag = False
        pygame.mouse.set_visible(True)      #设置鼠标可见


def check_aliens_bottome(ai_settings,screen,bullets,aliens,states,ship,score,attacks):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,states,screen,aliens,bullets,ship,score,attacks)
            break


def check_play_button(states,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,score,attacks):
    #当单机开始且游戏未开始时：
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not states.game_active:
        ai_settings.easy_flag=True
        ai_settings.initialize_dynamic_settings()       #重置速度
        check_button_work(screen, ship, aliens, bullets, score, ai_settings,states,attacks)


def check_difficult_button(states,difficult_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,score,attacks):
    if difficult_button.rect.collidepoint(mouse_x, mouse_y) and not states.game_active:
        ai_settings.difficult_flag = True
        ai_settings.difficult_dynamic_settings()
        check_button_work(screen, ship, aliens, bullets, score, ai_settings,states,attacks)


def check_button_work(screen,ship,aliens,bullets,score,ai_settings,states,attacks):
        # 重置游戏信息
        pygame.mouse.set_visible(False)  # 设置鼠标不可见
        states.reset_stats()
        states.game_active = True

        #重置图像
        score.prep_score()
        score.prep_level()
        score.prep_high_score()
        score.prep_ships()
        score.prep_bulletss(bullets)

        #清空编组
        aliens.empty()
        attacks.empty()
        bullets.empty()
        #重置外星人，并使飞船居中
        create_fleet(ai_settings,screen,states,aliens)
        ship.center_ship()


def check_high_score(states,score):
    #检查是否需要更新最高纪录
    if states.score >= states.high_score:
        states.high_score = states.score
        score.prep_high_score()

