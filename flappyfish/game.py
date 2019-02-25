import pygame as pg
from settings import *
from obj import *
import random

class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.clock = pg.time.Clock()
        self.canvas = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Verticality")
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        self.score = 0
        self.spike_pool = [0, 0, 0, 1]
        self.player_g = pg.sprite.Group()
        self.player = Player(WIDTH / 2, HEIGHT * 2 / 3)
        self.player_g.add(self.player)
        self.blocks = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.blocks.add(Block(0, 0))
        self.blocks.add(Block(WIDTH - 32, 0))
        self.blocks.add(Block(0, -640))
        self.upper = Block(0, -640)
        self.blocks.add(self.upper)
        self.blocks.add(Block(WIDTH - 32, - 640))
        self.init_spikes(self.upper)
        self.playing = True
        while self.playing:
            self.run()

    def run(self):
        self.clock.tick(FPS)
        self.events()
        self.update()
        self.fill()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.USEREVENT:
                temp_y = self.upper.rect.y
                self.upper = Block(0, temp_y - 640)
                self.blocks.add(self.upper)
                self.blocks.add(Block(WIDTH - 32, temp_y - 640))
                self.init_spikes(self.upper)
            if event.type == pg.USEREVENT + 1:
                self.playing = False

    def update(self):
        self.player_g.update()
        self.blocks.update()
        self.spikes.update()
        self.score += 1
        if pg.sprite.spritecollide(self.player, self.spikes, False, pg.sprite.collide_rect):
            self.playing = False

    def fill(self):
        self.canvas.fill(BG)

    def draw(self):
        self.player_g.draw(self.canvas)
        self.blocks.draw(self.canvas)
        self.spikes.draw(self.canvas)
        self.do_text(str(self.score), 30, BLACK, WIDTH / 2, 30)
        pg.display.flip()

    def init_spikes(self, upper):
        for i in range(int(self.upper.rect.top/32), int(self.upper.rect.bottom/32)):
            if random.choice(self.spike_pool):
                self.spikes.add(Spike(32, i*32, True))
            if random.choice(self.spike_pool):
                self.spikes.add(Spike(WIDTH - 64, i*32, False))

    def do_text(self, text, size, text_color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

game = Game()
while game.running:
    game.new()
