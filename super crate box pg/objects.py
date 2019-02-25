import pygame as pg
from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, canvas, img_path, x, y, type):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

class Player(pg.sprite.Sprite):
    def __init__(self, canvas, img_path, x, y, blocks, enemies, crates):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.in_air = True
        self.can_jump = False
        self.speed = P_SPEED
        self.direction = 0
        self.blocks = blocks
        self.enemies = enemies
        self.crates = crates
        self.weapon = None
        self.can_shoot = True
        self.facing = 1
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction = -1
            self.facing = -1
        if keys[pg.K_RIGHT]:
            self.direction = 1
            self.facing = 1
        self.vel_x = self.direction * self.speed
        if keys[pg.K_UP] and self.can_jump:
            self.vel_y -= JUMP
            self.in_air = True
            self.can_jump = False
        if keys[pg.K_x] and self.can_shoot:
            self.weapon.shoot()
            self.vel_x -= self.weapon.recoil * self.facing
            self.can_shoot = False
        if self.in_air:
            self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.direction = 0
        self.check_collisions()
        if self.rect.top >= HEIGHT:
            event = pg.event.Event(PLAYER_DEATH)
            pg.event.post(event)

    def check_collisions(self):
        for block in self.blocks:
            if pg.sprite.collide_rect(self, block):
                if self.rect.top <= block.rect.bottom and block.rect.top < self.rect.top and block.type == "platform":
                    self.rect.top = block.rect.bottom
                    self.vel_y = - self.vel_y
                if self.rect.bottom >= block.rect.top and block.rect.bottom > self.rect.bottom and block.type == "platform":
                    self.rect.bottom = block.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                if self.rect.left <= block.rect.right and block.rect.left < self.rect.left and block.type == "wall":
                    self.rect.left = block.rect.right
                if self.rect.right >= block.rect.left and block.rect.right > self.rect.right and block.type == "wall":
                    self.rect.right = block.rect.left
        for enemy in self.enemies:
            if pg.sprite.collide_rect(self, enemy):
                event = pg.event.Event(PLAYER_DEATH)
                pg.event.post(event)
        for crate in self.crates:
            if pg.sprite.collide_rect(self, crate):
                self.can_shoot = True
                event = pg.event.Event(CRATE_PICKUP, caller = crate)
                pg.event.post(event)

class Enemy(pg.sprite.Sprite):
    def __init__(self, canvas, blocks, projectiles):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice((True, False))
        if self.type:
            self.image = pg.image.load("img\\enemysmall.png")
            self.hp = SMALL_HP
            self.speed = SMALL_SPEED
        elif not self.type:
            self.image = pg.image.load("img\\enemybig.png")
            self.hp = BIG_HP
            self.speed = BIG_SPEED
        self.blocks = blocks
        self.projectiles = projectiles
        self.flaming = False
        self.in_air = True
        self.rect = self.image.get_rect()
        self.rect.center = SPAWN_POS
        self.direction = random.choice((-1, 1))
        self.vel_y = 0
        pg.time.set_timer(SPAWN_ENEMY, random.choice([2000, 3000, 4000]))
    def update(self):
        if self.in_air:
            self.vel_y += GRAVITY
        self.rect.x += self.direction * self.speed
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT:
            self.rect.center = SPAWN_POS
            if not self.flaming:
                self.flaming = True
                self.speed *= 2
        self.check_collisions()

    def check_collisions(self):
        for block in self.blocks:
            if pg.sprite.collide_rect(self, block):
                if self.rect.top <= block.rect.bottom and block.rect.top < self.rect.top and block.type == "platform":
                    self.rect.top = block.rect.bottom
                    self.vel_y = - self.vel_y
                if self.rect.bottom >= block.rect.top and block.rect.bottom > self.rect.bottom and block.type == "platform":
                    self.rect.bottom = block.rect.top
                    self.vel_y = 0
                if self.rect.left <= block.rect.right and block.rect.left < self.rect.left and block.type == "wall":
                    self.rect.left = block.rect.right
                    self.direction = - self.direction
                if self.rect.right >= block.rect.left and block.rect.right > self.rect.right and block.type == "wall":
                    self.rect.right = block.rect.left
                    self.direction = - self.direction
            elif not pg.sprite.collide_rect(self, block):
                self.in_air = True
        for projectile in self.projectiles:
            if pg.sprite.collide_rect(self, projectile):
                self.hp -= projectile.damage
                if self.hp <= 0:
                    event = pg.event.Event(ENEMY_DEATH, caller = (self, projectile))
                    pg.event.post(event)
                event = pg.event.Event(BULLET_HIT, caller = projectile)
                pg.event.post(event)


class Crate(pg.sprite.Sprite):
    def __init__(self, crate_spawn):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\crate.png")
        self.rect = self.image.get_rect()
        self.rect.center = crate_spawn

class Weapon(pg.sprite.Sprite):
    def __init__(self, bullet_type, reload_time, bullet_speed, bullets_per_shot, spread, damage, bullet_lifetime, knockback, recoil, blocks, player, projectiles):
        self.reload_time = reload_time
        self.bullet_speed = bullet_speed
        self.bullets_per_shot = bullets_per_shot
        self.spread = spread
        self.damage = damage
        self.knockback = knockback
        self.recoil = recoil
        self.bullet_type = bullet_type
        self.bullet_lifetime = bullet_lifetime
        self.player = player
        self.blocks = blocks
        self.projectiles = projectiles
    def shoot(self):
        for bullet in range(self.bullets_per_shot):
            dir_x = self.player.facing
            dir_y = random.uniform(-self.spread, self.spread)
            length = (dir_x ** 2 + dir_y ** 2) ** 0.5
            dir_x /= length
            dir_y /= length
            print(dir_x, dir_y)
            self.projectiles.add(Projectile(self.player, self.bullet_type, dir_x, dir_y, self.bullet_speed, self.bullet_lifetime, self.damage, self.blocks, self.knockback))
        pg.time.set_timer(RELOAD, self.reload_time)


class Projectile(pg.sprite.Sprite):
    def __init__(self, player, bullet_type, dir_x, dir_y, speed, lifetime, damage, blocks, knockback):
        pg.sprite.Sprite.__init__(self)
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = speed
        self.lifetime = lifetime
        self.damage = damage
        self.image = pg.image.load(bullet_type)
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.knockback = knockback
        self.blocks = blocks
    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
        self.check_collisions()
    def check_collisions(self):
        for block in self.blocks:
            if pg.sprite.collide_rect(self, block):
                event = pg.event.Event(BULLET_HIT, caller = self)
                pg.event.post(event)
