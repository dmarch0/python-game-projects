import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\player.png")
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.vel_y = 0
        self.vel_x = P_SPEED
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.vel_y -= JUMP_FORCE
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.right >= WIDTH - 32:
            self.rect.right = WIDTH - 32
            self.vel_x = - self.vel_x
        if self.rect.left <= 32:
            self.rect.left = 32
            self.vel_x = - self.vel_x
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            event = pg.event.Event(pg.USEREVENT + 1)
            pg.event.post(event)

class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\block.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.y += GAME_SPEED
        if self.rect.top >= HEIGHT:
            event = pg.event.Event(pg.USEREVENT)
            pg.event.post(event)
            self.kill()


class Spike(pg.sprite.Sprite):
    def __init__(self, x, y, left):
        pg.sprite.Sprite.__init__(self)
        if left:
            self.image = pg.image.load("img\\spikesleft.png")
        elif not left:
            self.image = pg.image.load("img\\spikesright.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.y += GAME_SPEED
        if self.rect.top >= HEIGHT:
            self.kill()
