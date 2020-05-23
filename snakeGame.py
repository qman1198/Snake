import pygame as pg
import numpy as np


width = 600
height = 600
scl = 15
black = 0, 0, 0
white = 255, 255, 255
fps = 100
speed = 20


pg.init()
screen = pg.display.set_mode((width, height)) 
running = True
paused = False

def dist(ax, ay, bx, by):
    a = np.array((ax, ay))
    b = np.array((bx, by))
    return np.linalg.norm(a-b)
def gameOver(s):
    print("Score: ", s.length)
    pg.time.wait(400)
    pg.display.quit()
class Snake():
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.i = x // scl
        self.j = y //scl
        self.rects = [pg.Rect(x,y,scl,scl), pg.Rect(x - scl,y,scl,scl), pg.Rect(x - (2*scl),y,scl,scl), pg.Rect(x - (3*scl),y,scl,scl)]
        self.length = 4
        self.dir = [0,0]
    def grow(self):
        self.length += 1
        self.rects.append(pg.Rect(width + 1,height + 1,scl,scl))
    def update(self):
        x_0 = self.x
        y_0 = self.y
        self.j = self.j + self.dir[0]*speed/100
        self.i = self.i + self.dir[1]*speed/100
        self.y = scl*np.floor(self.j)
        self.x = scl*np.floor(self.i)
        if self.x != x_0 or self.y != y_0: 
            for i in reversed(range(1,self.length)):
                self.rects[i] = self.rects[i - 1]
            self.rects[0] = pg.Rect(self.x,self.y,scl,scl)
    def draw(self, screen):
        for rect in self.rects:
            pg.draw.rect(screen, white, rect)

class Fruit():
    def __init__(self):
        self.x = scl*np.floor(np.random.randint(1,width//scl - 1))
        self.y = scl*np.floor(np.random.randint(1,height//scl - 1))
        self.rect = pg.Rect(self.x,self.y,scl,scl)
        self.clr = pg.Color(255,255,255)
        self.clr.hsva = (np.random.randint(0,360), 100, 100, 100)
    def draw(self, screen):
        pg.draw.rect(screen, self.clr, self.rect)

startX = scl*np.random.randint(1,width//scl - 1)
startY = scl*np.random.randint(1,height//scl - 1)
s = Snake(startY, startX)
f = Fruit()
clock = pg.time.Clock()
while running:
    dt = clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            running = False
        elif event.type == pg.KEYDOWN:
            if pg.key.get_pressed()[pg.K_SPACE]:
                paused = not(paused)
            if pg.key.get_pressed()[pg.K_w] and s.dir != [1, 0]:
                s.dir = [-1, 0]
            if pg.key.get_pressed()[pg.K_d] and s.dir != [0, -1]:
                s.dir = [0, 1]
            if pg.key.get_pressed()[pg.K_s] and s.dir != [-1, 0]:
                s.dir = [1, 0]
            if pg.key.get_pressed()[pg.K_a] and s.dir != [0, 1]:
                s.dir = [0, -1]
            if pg.key.get_pressed()[pg.K_SPACE] and s.dir != [0, 1]:
                s.grow()

    if s.rects[0].left < 0 or s.rects[0].right > width or s.rects[0].top < 0 or s.rects[0].bottom > height:
        s.dir = [0,0]
        gameOver(s)
        running = False
        break
    if(dist(f.x,f.y,s.x, s.y) < 1):
            s.grow()
            f = Fruit()
    s.update()
    for i in range(2,s.length):
        if dist(s.rects[0].x,s.rects[0].y,s.rects[i].x,s.rects[i].y) < 1:
            s.dir = [0,0]
            gameOver(s)
            running = False
            break
    screen.fill(black)
    s.draw(screen)
    f.draw(screen)
    pg.display.flip()
