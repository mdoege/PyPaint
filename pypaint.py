#!/usr/bin/env python

# Paint program

import pygame, numpy, os, sys, time, random, math

# canvas size
RES = 1200, 800

# brush size (large)
BRUSH = 21

# brush size (small)
BRUSH_SMALL = 7

# line size (large)
LSIZE = 14

# line size (small)
LSIZE_SMALL = 4

# airbrush density
AIRDENS = 10

# airbrush dot size
AIRSIZE = 4

# palette box size
PALBW = 50

# palette columns
PALHE = 3

# background color
COLBG = 0x202020

# color palettes in RGB hex:

# default colors
cols_s = [
0,
0x404040, # black, white, and grays
0x606060,
0x808080,
0xa0a0a0,
0xb0b0b0,
0xd0d0d0,
0xffffff,
0xff0000, # full-intensity colors
0xffb000,
0x00ff00,
0x0000ff,
0xffff00,
0x00ffff,
0xff00ff,
0xaa0000, # darker colors
0x884000,
0x00aa00,
0x0000aa,
0xaaaa00,
0x00aaaa,
0xaa00aa,
0xff8080, # pastel colors
0xffd080,
0x80ff80,
0x8080ff,
0xffff80,
0x80ffff,
0xff80ff,
]

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

# DPaint
cols_d = [
0,
0xa0a0a0,
0xee0000,
0xaa0000,
0xdd8800,
0xffee00,
0x88ff00,
0x008800,
0x00bb66,
0x00dddd,
0x00aaff,
0x0077cc,
0x0000ff,
0x7700ff,
0xcc00ee,
0xcc0088,
0x662200,
0xee5522,
0xaa5522,
0xffccaa,
0x333333,
0x444444,
0x555555,
0x666666,
0x777777,
0x888888,
0x999999,
0xaaaaaa,
0xcccccc,
0xdddddd,
0xeeeeee,
0xffffff,
]

# MS Paint classic
cols_msp = [
0xffffff,
0,
0xc0c0c0,
0x808080,
0xff0000,
0x800000,
0xffff00,
0x808000,
0x00ff00,
0x008000,
0x00ffff,
0x008080,
0x0000ff,
0x000080,
0xff00ff,
0x800080,
0xffff80,
0x808040,
0x00ff80,
0x004040,
0x80ffff,
0x0080ff,
0x8080ff,
0x004080,
0xff0080,
0x400080,
0xff8040,
0x804000,
]

# Pinta
cols_pt = [
0xffffff,
0x000000,
0xa0a0a0,
0x808080,
0x404040,
0x303030,
0xff0000,
0xff7f7f,
0xff6a00,
0xffb27f,
0xffd800,
0xffe97f,
0xb6ff00,
0xdaff7f,
0x4cff00,
0xa5ff7f,
0x00ff21,
0x7fff8e,
0x00ff90,
0x7fffc5,
0x00ffff,
0x7fffff,
0x0094ff,
0x7fc9ff,
0x0026ff,
0x7f92ff,
0x4800ff,
0xa17fff,
0xb200ff,
0xd67fff,
0xff00dc,
0xff7fed,
0xff006e,
0xff7fb6,
]

# Mostly empty palette (meant for picking colors from images)
cols_pick = [
0,
0xffffff,
]

# palettes and palette names
palettes =  cols_s,    cols_g,  cols_p,   cols_d,   cols_msp,   cols_pt, cols_pick
palnames = "default", "GNOME", "PICO-8", "DPaint", "MS Paint", "Pinta", "empty"

# tool names
tname = "dotted freehand", "continuous freehand", "straight lines", "airbrush", "fill tool"

# icon images
icons = []
for n in range(5):
    p = "%u.png" % n
    img = pygame.image.load(os.path.join("img", p))
    icons.append(img)
brico_s = pygame.image.load(os.path.join("img", "brsmall.png"))
brico_b = pygame.image.load(os.path.join("img", "brbig.png"))
b_undo  = pygame.image.load(os.path.join("img", "undo.png"))

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
        self.screen = pygame.display.set_mode((RES[0] + PALHE * PALBW, RES[1]))
        self.clock = pygame.time.Clock()
        if len(sys.argv) > 1:
            self.img = pygame.image.load(sys.argv[1]).convert()
            w, h = self.img.get_size()
            if w > RES[0] or h > RES[1]:
                asp_can = RES[0] / RES[1]
                asp_img = w / h

                # scale to fit canvas
                if asp_img > asp_can:
                    w = RES[0]
                    h = RES[0] / asp_img
                else:
                    w = RES[1] * asp_img
                    h = RES[1]
                self.img = pygame.transform.smoothscale(self.img, (w, h))
        else:
            self.img = pygame.Surface(RES)
            self.img.fill(0xffffff)
        self.mdown = False
        self.palnum = 0
        self.cols = palettes[self.palnum]
        self.col = 0
        self.colpic = pygame.Surface((PALHE * PALBW, RES[1]))
        self.getcolpic()
        self.undo = [self.img.copy()]
        self.tool = 1
        self.small_brush = True
        self.line_start = 0, 0
        self.hide = False
        self.title()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.undo.append(self.img.copy())
                self.img.fill(0xffffff)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.image.save(self.img,
                        time.strftime("%y%m%d_%H%M%S.png"))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.mouse.get_pos()[0] < RES[0]:
                    self.mdown = True
                    self.lastpos = pygame.mouse.get_pos()
                    if self.tool == 2:  # straight lines
                        self.line_start = pygame.mouse.get_pos()
                elif event.button == 1 and not self.hide:
                    xp, yp = pygame.mouse.get_pos()
                    xp -= RES[0]
                    yp -= 50
                    xp = xp // PALBW
                    yp = yp // PALBW
                    v = RES[1] // PALBW - 1
                    c = v * xp + yp
                    if yp >= 0 and c < len(self.cols):
                        self.col = c
                        self.getcolpic()
                    if yp < 0 and xp == 0:
                        self.small_brush = not self.small_brush
                        self.title()
                    if yp < 0 and xp == 1:
                        self.tool += 1
                        if self.tool > len(tname) - 1:
                            self.tool = 0
                        self.title()
                    if yp < 0 and xp == 2:
                        if len(self.undo) >= 2:
                            self.img = self.undo[-2].copy()
                            self.undo = [self.undo[-1], self.undo[-2]]
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
                    if self.tool == 2 and pygame.mouse.get_pos()[0] < RES[0]: # straight lines
                        if self.small_brush: br = LSIZE_SMALL
                        else: br = LSIZE
                        pygame.draw.line(self.img, self.cols[self.col],
                            self.line_start, pygame.mouse.get_pos(), width = br)
                    if pygame.mouse.get_pos()[0] < self.img.get_size()[0]:
                        self.undo.append(self.img.copy())
                        if len(self.undo) > 2:
                            self.undo = self.undo[-2:]
            if event.type == pygame.MOUSEWHEEL:
                self.col -= event.y
                self.col = self.col % len(self.cols)
                self.getcolpic()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.palnum += 1
                if self.palnum >= len(palettes):
                    self.palnum = 0
                self.cols = palettes[self.palnum]
                self.col = 0
                self.getcolpic()
                self.title()
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                if len(self.undo) >= 2:
                    self.img = self.undo[-2].copy()
                    self.undo = [self.undo[-1], self.undo[-2]]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                pos = pygame.mouse.get_pos()
                try:
                    c = self.img.get_at(pos)
                except:
                    pass
                else:
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
        self.colpic.fill(COLBG)
        v = RES[1] // PALBW - 1
        for x in range(PALHE):
            for y in range(v):
                i = v * x + y
                if i < len(self.cols):
                    pygame.draw.rect(self.colpic, self.cols[i],
                    [PALBW * x, PALBW * y, PALBW, PALBW])
                if i == self.col:
                    pygame.draw.rect(self.colpic, 0,
                    [PALBW * x, PALBW * y, PALBW, PALBW],
                    width = 2)
                    pygame.draw.rect(self.colpic, "0xffffff",
                    [PALBW * x + 2, PALBW * y + 2, PALBW - 4, PALBW - 4],
                    width = 4)
                    pygame.draw.rect(self.colpic, 0,
                    [PALBW * x + 6, PALBW * y + 6, PALBW - 12, PALBW - 12],
                    width = 2)

    def title(self):
        if self.small_brush:
            bb = ", small brush"
        else:
            bb = ", large brush"
        if self.tool == 4:  # flood fill
            bb = ""
        pygame.display.set_caption(f'Paint ({tname[self.tool]}{bb}, {palnames[self.palnum]} palette)')

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
            elif self.tool == 3: # airbrush
                for n in range(AIRDENS):
                    phi = random.uniform(0, 2 * math.pi)
                    r = random.gauss(0, brsize)
                    if abs(r) <= 2 * brsize:
                        pygame.draw.rect(self.img, self.cols[self.col],
                        [x + r * math.sin(phi), y + r * math.cos(phi),
                            AIRSIZE, AIRSIZE])
            elif self.tool == 4: # flood fill
                fill(self.img, (x, y), self.cols[self.col])

        self.screen.fill(COLBG)
        self.screen.blit(self.img, (0, 0))
        if self.tool == 2 and self.mdown: # straight lines
            if self.small_brush: br = LSIZE_SMALL
            else: br = LSIZE
            pygame.draw.line(self.screen, self.cols[self.col],
                self.line_start, pygame.mouse.get_pos(), width = br)
        if not self.hide:
            self.screen.blit(self.colpic, (RES[0], 50))
            self.screen.blit(icons[self.tool], (RES[0] + 50, 0))
            self.screen.blit(b_undo, (RES[0] + 100, 0))
            if self.small_brush:
                self.screen.blit(brico_s, (RES[0], 0))
            else:
                self.screen.blit(brico_b, (RES[0], 0))
        pygame.display.flip()

c = Paint()
c.run()

