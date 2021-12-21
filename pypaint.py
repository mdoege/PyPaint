#!/usr/bin/env python

# Paint program

import pygame, numpy, sys, time, random, math

# canvas size
RES = 1200, 800

# brush size (normal)
BRUSH = 21

# brush size (small)
BRUSH_SMALL = 7

# airbrush density
AIRDENS = 10

# airbrush dot size
AIRSIZE = 4

# color palettes in RGB hex:

# GNOME
cols_g = [
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
]

# PICO-8
cols_p = [
0,
0xffffff,
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
]

tname = "Dotted Freehand", "Continuous Freehand", "Airbrush", "Fill Tool"

# modified version of code at
# https://stackoverflow.com/questions/41656764/how-to-implement-flood-fill-in-a-pygame-surface
def fill(surface, position, fill_color):
    w, h = surface.get_size()
    surf_array = pygame.surfarray.pixels2d(surface)
    orig = surf_array[position]
    grid = numpy.zeros((w, h), dtype = int)
    grid[:,:] = 1
    frontier = [position]
    while len(frontier) > 0:
        # protect against out of memory errors due to runaway filling:
        if len(frontier) > w * h:
            print("STOP FILL")
            pygame.surfarray.blit_array(surface, surf_array)
            del surf_array
            return
        x, y = frontier.pop()
        surf_array[x, y] = fill_color
        grid[x,y] = 0
        if x < w - 1 and surf_array[x + 1, y] == orig and grid[x + 1, y]:
            frontier.append((x + 1, y))
            grid[x + 1, y] = 0
        if x > 0 and surf_array[x - 1, y] == orig and grid[x - 1, y]:
            frontier.append((x - 1, y))
            grid[x - 1, y] = 0
        if y < h - 1 and surf_array[x, y + 1] == orig and grid[x, y + 1]:
            frontier.append((x, y + 1))
            grid[x, y + 1] = 0
        if y > 0 and surf_array[x, y - 1] == orig and grid[x, y - 1]:
            frontier.append((x, y - 1))
            grid[x, y - 1] = 0

    del surf_array

class Paint:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        if len(sys.argv) > 1:
            self.img = pygame.image.load(sys.argv[1]).convert()
        else:
            self.img = pygame.Surface(RES)
            self.img.fill(0xffffff)
        self.mdown = False
        self.cols = cols_g
        self.col = 0
        self.colpic = pygame.Surface((50, 50))
        self.getcolpic()
        self.tool = 0
        self.small_brush = False
        self.hide = False
        self.title()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.img.fill(0xffffff)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.image.save(self.img,
                        time.strftime("%y%m%d_%H%M%S.png"))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mdown = True
                    self.lastpos = pygame.mouse.get_pos()
                elif event.button == 2:
                    self.small_brush = not self.small_brush
                    self.title()
                elif event.button == 3:
                    self.tool += 1
                    if self.tool > len(tname) - 1:
                        self.tool = 0
                    self.title()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mdown = False
            if event.type == pygame.MOUSEWHEEL:
                self.col -= event.y
                self.col = self.col % len(self.cols)
                self.getcolpic()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.cols = cols_p
                self.getcolpic()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.tool += 1
                if self.tool > len(tname) - 1:
                    self.tool = 0
                self.title()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.small_brush = not self.small_brush
                self.title()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                self.hide = not self.hide
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                pos = pygame.mouse.get_pos()
                c = self.img.get_at(pos)
                ch = c[0] * (256**2) + c[1] * 256 + c[2]
                in_pal = False
                for n, col in enumerate(self.cols):
                    if ch == col:
                        self.col = n
                        in_pal = True
                        self.getcolpic()
                if not in_pal:
                    self.cols.append(ch)
                    self.col = len(self.cols) - 1
                    self.getcolpic()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(50)
            self.events()
            self.update()
        pygame.quit()

    def getcolpic(self):
        self.colpic.fill(self.cols[self.col])

    def title(self):
        if self.small_brush:
            bb = ", small brush"
        else:
            bb = ", large brush"
        if self.tool == 3:
            bb = ""
        pygame.display.set_caption(f'Paint ({tname[self.tool]}{bb})')

    def update(self):
        if self.mdown:
            if self.small_brush:
                brsize = BRUSH_SMALL
            else:
                brsize = BRUSH
            x, y = pygame.mouse.get_pos()
            if self.tool == 0:   # pen (aka dotted freehand in Deluxe Paint)
                pygame.draw.rect(self.img, self.cols[self.col],
                    [x - brsize // 2, y - brsize // 2, brsize, brsize])
            elif self.tool == 1: # pen (lines)
                steps = max(1, abs(x - self.lastpos[0]),
                        abs(y - self.lastpos[1]))
                for n in range(steps):
                    xp = self.lastpos[0] + n * (x - self.lastpos[0]) / steps
                    yp = self.lastpos[1] + n * (y - self.lastpos[1]) / steps
                    pygame.draw.rect(self.img, self.cols[self.col],
                        [xp - brsize // 2, yp - brsize // 2, brsize, brsize])
                self.lastpos = x, y
            elif self.tool == 2: # airbrush
                for n in range(AIRDENS):
                    phi = random.uniform(0, 2 * math.pi)
                    r = random.gauss(0, brsize)
                    pygame.draw.rect(self.img, self.cols[self.col],
                        [x + r * math.sin(phi), y + r * math.cos(phi),
                            AIRSIZE, AIRSIZE])
            elif self.tool == 3: # flood fill
                fill(self.img, (x, y), self.cols[self.col])

        self.screen.blit(self.img, (0, 0))
        if not self.hide:
            self.screen.blit(self.colpic, (0, 0))
        pygame.display.flip()

c = Paint()
c.run()

