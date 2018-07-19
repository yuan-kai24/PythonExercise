import pygame
from pygame.locals import *
from random import randint

WIDTH = 1200
HEIGHT = 600

class Person:
    def __init__(self):
        self.user = pygame.image.load("./resource/user.png")
        self.user_rect = self.user.get_rect()
        self.user_rect.top = HEIGHT / 2 - self.user_rect.height / 2
        self.isMove_UP = False
        self.isMove_DOWN = False
        self.isbullet_dis = False

    def display(self):
        Form.blit(self.user, self.user_rect)

    def move(self):
        if self.isMove_UP and self.user_rect.top > 0:
            self.user_rect.move_ip(0, -5)
        elif self.isMove_DOWN and self.user_rect.top < HEIGHT - self.user_rect.height:
            self.user_rect.move_ip(0, 5)

        Bullet.interval += 1
        if Bullet.interval > 10 and self.isbullet_dis:
            self.show_bullet()
            Bullet.interval = 0

    def show_bullet(self):
        bullet = Bullet()
        bullet.bul_rect.top = self.user_rect.top + self.user_rect.height/2 - bullet.bul_rect.height/2
        bullet.bul_rect.left = self.user_rect.width
        Bullet.bullet_list.append(bullet)

class Bullet:
    bullet_list = []
    interval = 0
    def __init__(self):
        self.bul = pygame.image.load("./resource/zd.png")
        self.bul_rect = self.bul.get_rect()

    def bulletmove(self):
        self.bul_rect.move_ip(10, 0)
        if self.bul_rect.left > WIDTH:
            Bullet.bullet_list.remove(self)
        for itemboos in Boos.boos_list:
            if self.bul_rect.colliderect(itemboos.boos_rect):
                Boos.boos_list.remove(itemboos)
                Bullet.bullet_list.remove(self)
                break

    def display(self):
        Form.blit(self.bul, self.bul_rect)

class Boos:
    boos_list = []
    interval = 0
    def __init__(self):
        self.boos = pygame.image.load("./resource/boos.png")
        self.boos_rect = self.boos.get_rect()
        self.boos_rect.move_ip(WIDTH, randint(0, 500))

    def boosmove(self):
        self.boos_rect.move_ip(-15, 0)
        if self.boos_rect.left < 0:
            Boos.boos_list.remove(self)
        if self.boos_rect.colliderect(peas.user_rect):
            pygame.quit()
            exit()

    def display(self):
        Form.blit(self.boos, self.boos_rect)

if __name__ == '__main__':

    Form = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.image.load("./resource/bk.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    peas = Person()

    clock = pygame.time.Clock()

    while True:
        Form.blit(background, background_rect)
        peas.display()

        # 子弹移动
        for bullet in Bullet.bullet_list:
            bullet.display()
            bullet.bulletmove()

        # boos移动
        for boos in Boos.boos_list:
            boos.display()
            boos.boosmove()

        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                # 移动和发射
                if event.key == K_UP or event.key == K_w:
                    peas.isMove_UP = True
                elif event.key == K_DOWN or event.key == K_s:
                    peas.isMove_DOWN = True
                if event.key == K_SPACE:
                    peas.isbullet_dis = True
            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    peas.isMove_UP = False
                elif event.key == K_DOWN or event.key == K_s:
                    peas.isMove_DOWN = False
                if event.key == K_SPACE:
                    peas.isbullet_dis = False

        Boos.interval += 1
        if Boos.interval > 10:
            Boos.interval = 0
            boos = Boos()
            Boos.boos_list.append(boos)
        peas.move()

        clock.tick(60)
        pygame.display.update()