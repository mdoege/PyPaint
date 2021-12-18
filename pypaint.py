#!/usr/bin/env python

# Paint program

import pygame, time, random, math

# canvas size
RES = 1200, 800

# brush size
BRUSH = 21

# airbrush density
AIRDENS = 10

# airbrush dot size
AIRSIZE = 4

# color palettes in RGB hex:

# GNOME
cols_g = (
0,
0xffffff,
0x555753,
0xcc0000,
0xf57900,
0xedd400,
0x73d216,
0x3465a4,
0x75507b,
0xc17d11,
)

# PICO-8
cols_p = (
0,
0x1d2b53,
0x7e2553,
0x008751,
0xab5236,
0x5f574f,
0xc2c3c7,
0xfff1e8,
0xff004d,
0xffa300,
0xffec27,
0x00e436,
0x29adff,
0x83769c,
0xff77a8,
0xffccaa,
)

class Paint:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption('Paint')
        self.clock = pygame.time.Clock()
        self.img = pygame.Surface(RES)
        self.img.fill(0xffffff)
        self.mdown = False
        self.cols = cols_g
        self.col = 0
        self.colpic = pygame.Surface((50, 50))
        self.getcolpic()
        self.tool = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.img.fill(0xffffff)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.image.save(self.img,
                        time.strftime("%y%m%d_%H%M%S.png"))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mdown = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mdown = False
            if event.type == pygame.MOUSEWHEEL:
                self.col -= event.y
                self.col = self.col % len(self.cols)
                self.getcolpic()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.cols = cols_p
                self.getcolpic()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.tool = not self.tool

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(50)
            self.events()
            self.update()
        pygame.quit()

    def getcolpic(self):
        self.colpic.fill(self.cols[self.col])

    def update(self):
        if self.mdown:
            x, y = pygame.mouse.get_pos()
            if not self.tool:   # pen (aka dotted freehand in Deluxe Paint)
                pygame.draw.rect(self.img, self.cols[self.col],
                    [x - BRUSH // 2, y - BRUSH // 2, BRUSH, BRUSH])
            else:               # airbrush
                for n in range(AIRDENS):
                    phi = random.uniform(0, 2 * math.pi)
                    r = random.gauss(0, BRUSH)
                    pygame.draw.rect(self.img, self.cols[self.col],
                        [x + r * math.sin(phi), y + r * math.cos(phi),
                            AIRSIZE, AIRSIZE])

        self.screen.blit(self.img, (0, 0))
        self.screen.blit(self.colpic, (0, 0))
        pygame.display.flip()

c = Paint()
c.run()

