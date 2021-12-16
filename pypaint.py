#!/usr/bin/env python

# Paint program

import pygame, time

# canvas size
RES = 1200, 800

# brush size
BRUSH = 21

# color palette in RGB hex:
cols = (
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

class Paint:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption('Paint')
        self.clock = pygame.time.Clock()
        self.img = pygame.Surface(RES)
        self.img.fill(0xffffff)
        self.mdown = False
        self.col = 0
        self.colpic = pygame.Surface((50, 50))
        self.getcolpic()

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
                self.col += event.y
                self.col = self.col % len(cols)
                self.getcolpic()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(50)
            self.events()
            self.update()
        pygame.quit()

    def getcolpic(self):
        self.colpic.fill(cols[self.col])

    def update(self):
        if self.mdown:
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(self.img, cols[self.col],
                [x - BRUSH // 2, y - BRUSH // 2, BRUSH, BRUSH])

        self.screen.blit(self.img, (0, 0))
        self.screen.blit(self.colpic, (0, 0))
        pygame.display.flip()

c = Paint()
c.run()

