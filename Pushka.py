#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
from random import randint
from random import choice

import pygame


FPS = 250

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, vx, vy, r):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = 40
        self.y = 450
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = choice(GAME_COLORS)
        self.g = 10
        
    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.g/FPS
        self.x += self.vx/FPS
        self.y -= self.vy/FPS - self.g/(FPS**2)*2
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.vx = -self.vx
        if self.y + self.r >= HEIGHT or self.y - self.r <= 0:
            self.vy = -self.vy
            
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class Gun:
    def __init__(self, screen):
        self.x = 40
        self.y = 450
        self.r = 10
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        vx = self.f2_power * math.cos(self.an)
        vy = - self.f2_power * math.sin(self.an)
        new_ball = Ball(self.screen, vx, vy, randint(2, 35))
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        
    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
            
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    
    
class circle_target:
    def __init__(self):
        self.x = randint(300, 600)
        self.y = randint(300, 600)
        self.r = randint(2, 50)
        self.color = 1
        self.points = 0

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(300, 600)
        self.y = randint(300, 600)
        self.r = randint(2, 50)
        self.color = 1
        
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        
    def is_hit(self, ball):
        '''
        Проверяет есть ли попадание шарика по круговой цели.
        '''
        return ((ball.x - self.x)**2 + (ball.y - self.y)**2)**0.5 <= ball.r + self.r
        
        
class rectangle_target:
    def __init__(self):
        self.x = randint(300, 600)
        self.y = randint(300, 600)
        self.color = 1
        self.a = randint(2, 50)
        self.points = 0

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(300, 600)
        self.y = randint(300, 600)
        self.r = randint(2, 50)
        self.color = 1
        
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - self.a/2, self.y - self.a/2, self.a, self.a))
        
    def is_hit(self, ball):
        '''
        Проверяет есть ли попадание шарика по квадратной цели.
        '''
        return self.x - self.a/2 - ball.r <= ball.x <= self.x + self.a/2 + ball.r and self.y - self.a/2 - ball.r <= ball.y <= self.y + self.a/2 + ball.r

    
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
ball = Ball()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
        b.move()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    i = 0
    while i < len(balls):
        if balls[i].is_hit(ball):
            balls.remove(balls[i])
            target.hit()
            target.new_target()
            i -= 1
            break
        i += 1            
    gun.power_up()

pygame.quit()

