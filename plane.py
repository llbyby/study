# -*- coding: utf-8 -*-
import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((600, 800), 0, 32)
player = "古力"
pygame.display.set_caption("Hello,Lawrence")
background = pygame.image.load('static/planepic/background.png').convert()
font = pygame.font.SysFont('microsoftyahei', 32)

lawrence_start = pygame.image.load('static/planepic/lawrence_start.jpg').convert()
lawrence_end = pygame.image.load('static/planepic/lawrence_end.jpg').convert()

class Plane:
    def restart(self):
        self.x = 200
        self.y = 800

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('static/planepic/plane.png').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width() / 2
        y -= self.image.get_height() / 2
        self.x = x
        self.y = y

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('static/planepic/bullet.png').convert_alpha()
        self.active = False

    def move(self):
        if self.active:
            self.y -= 3
        if self.y < 0:
            self.active = False

    def restart(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        self.active = True

class Enemy:
    def restart(self):
        self.x = random.randint(50, 550)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.00

    def __init__(self):
        self.restart()
        self.image = pygame.image.load("static/planepic/enemy.png").convert_alpha()

    def move(self):
        if self.y < 1000:
            self.y += self.speed
        else:
            self.restart()

def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and \
            (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    return False

def checkCrash(enemy, plane):
    if (plane.x > enemy.x - 0.8 * plane.image.get_width()) and \
            (plane.x < enemy.x + enemy.image.get_width() - 0.2 * plane.image.get_width()) and \
            (plane.y > enemy.y - 0.8 * plane.image.get_height()) and \
            (plane.y < enemy.y + enemy.image.get_height() - 0.2 * plane.image.get_height()):
        return True
    return False

plane = Plane()

bullets = []
for i in range(5):
    bullets.append(Bullet())
count_b = len(bullets)
index_b = 0
interval_b = 0

enemies = []
for e in range(5):
    enemies.append(Enemy())

gameover = False
score = 0
bestscore = 0
times = 0
firsttime = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))

    if firsttime:
        starttext = font.render("你好，%s" % player, 1, (0, 0, 0))
        screen.blit(starttext, (225, 550))
        screen.blit(lawrence_start, (180, 200))
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN: firsttime = False
    else:
        if not gameover:
            interval_b -= 1
            if interval_b < 0:
                bullets[index_b].restart()
                interval_b = 100
                index_b = (index_b + 1) % count_b
            for b in bullets:
                if b.active:
                    for e in enemies:
                        if checkHit(e, b):
                            score += 1
                    b.move()
                    screen.blit(b.image, (b.x, b.y))

            for e in enemies:
                if checkCrash(e, plane):
                    gameover = True
                    times += 1
                e.move()
                screen.blit(e.image, (e.x, e.y))

            plane.move()
            screen.blit(plane.image, (plane.x, plane.y))

            text = font.render("Score:%d" % score, 1, (0, 0, 0))
            screen.blit(text, (0, 0))

            pygame.display.update()

        else:
            if score > bestscore: bestscore = score
            text = font.render("Score:%d  BestScore:%d" % (score, bestscore), 1, (0, 0, 0))
            screen.blit(text, (0, 0))
            endtext = font.render("扑街%d次，点击继续" % times, 1, (0, 0, 0))
            screen.blit(endtext, (160, 550))
            screen.blit(lawrence_end, (230,200))
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                plane.restart()
                for e in enemies:
                    e.restart()
                for b in bullets:
                    b.restart()
                index_b = 0
                interval_b = 0
                gameover = False
                score = 0