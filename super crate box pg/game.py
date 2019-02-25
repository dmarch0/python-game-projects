import pygame as pg
from settings import *
from objects import *

class Game:
    def __init__(self):
        pg.init()
        self.canvas = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Super Crate Box")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        self.score = 0
        self.crate_spawn_poss = []
        self.blocks = pg.sprite.Group()
        self.weapons = {}
        self.enemies = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.enemies.add(Enemy(self.canvas, self.blocks, self.projectiles))
        self.crates = pg.sprite.Group()
        self.init_level()
        self.crates.add(Crate(random.choice(self.crate_spawn_poss)))
        self.player = Player(self.canvas, "img\\player.png", START_POS_X, START_POS_Y, self.blocks, self.enemies, self.crates)
        self.init_weapons()
        self.player.weapon = self.weapons["pistol"]
        self.player_g = pg.sprite.Group()
        self.player_g.add(self.player)
        self.playing = True
        pg.display.flip()
        while self.playing:
            self.run()

    def run(self):
        self.clock.tick(FPS)
        self.events()
        self.update()
        self.fill()
        self.draw()

    def update(self):
        self.player.update()
        self.blocks.update()
        self.enemies.update()
        self.projectiles.update()
        self.crates.update()
        #print(self.clock.get_fps())

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == SPAWN_ENEMY:
                self.enemies.add(Enemy(self.canvas, self.blocks, self.projectiles))
            if event.type == PLAYER_DEATH:
                self.playing = False
            if event.type == ENEMY_DEATH:
                self.enemies.remove(event.caller[0])
                self.projectiles.remove(event.caller[1])
            if event.type == BULLET_HIT:
                self.projectiles.remove(event.caller)
            if event.type == RELOAD:
                self.player.can_shoot = True
            if event.type == CRATE_PICKUP:
                self.crates.remove(event.caller)
                self.crates.add(Crate(random.choice(self.crate_spawn_poss)))
                self.player.weapon = self.weapons[random.choice(list(self.weapons.keys()))]
                self.score +=1

    def fill(self):
        self.canvas.fill(BG)

    def draw(self):
        self.blocks.draw(self.canvas)
        self.enemies.draw(self.canvas)
        self.projectiles.draw(self.canvas)
        self.crates.draw(self.canvas)
        self.player_g.draw(self.canvas)
        self.do_text(str(self.score), 30, BLACK, WIDTH / 2, 30)
        pg.display.flip()


    def init_level(self):
        self.blocks.add(Block(self.canvas, "img\\leftwall.png", 0, 20, "wall"))
        self.blocks.add(Block(self.canvas, "img\\leftwall.png", 700, 20, "wall"))
        self.blocks.add(Block(self.canvas, "img\\bigplatform.png", 0, 0, "platform"))
        self.blocks.add(Block(self.canvas, "img\\bigplatform.png", 400, 0, "platform"))
        self.blocks.add(Block(self.canvas, "img\\bigplatform.png", 0, 460, "platform"))
        self.blocks.add(Block(self.canvas, "img\\bigplatform.png", 400, 460, "platform"))
        self.blocks.add(Block(self.canvas, "img\\bigplatform.png", 200, 130, "platform"))
        self.blocks.add(Block(self.canvas, "img\\bigplatform.png", 200, 350, "platform"))
        self.blocks.add(Block(self.canvas, "img\\smallplatform.png", 20, 240, "platform"))
        self.blocks.add(Block(self.canvas, "img\\smallplatform.png", 540, 240, "platform"))
        self.crate_spawn_poss = [(255, 115), (465, 115), (100, 225), (620, 225), (255, 335), (465, 335), (100, 445), (620, 445)]

    def init_weapons(self):
        #bullet sprite, reload time, bullet speed, bullets per shot, spread, damage, lifetime, knockback, recoil
        self.weapons["pistol"] = Weapon("img\\smallbullet.png", 200, 7, 1, 0, 10, 10000, 0, 0, self.blocks, self.player, self.projectiles)
        self.weapons["shotgun"] = Weapon("img\\smallbullet.png", 1000, 7, 8, 1, 5, 10000, 1, 10, self.blocks, self.player, self.projectiles)
        self.weapons["machinegun"] = Weapon("img\\smallbullet.png", 50, 7, 1, 0.1, 3, 10000, 1, 10, self.blocks, self.player, self.projectiles)

    def do_text(self, text, size, text_color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

game = Game()
while game.running:
    game.new()

pg.quit()
