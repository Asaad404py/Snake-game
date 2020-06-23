import pygame, math, random, sys
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows=20
    width=500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i = self.pos[0]
        j= self.pos[1]

        pygame.draw.rect(surface, self.color,(i*dis+0.5,j*dis+0.5,dis-0.5,dis-0.5))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i* dis + dis - radius*2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self,color,pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 1


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.turns[self.head.pos[:]] = [-1, 0]

                elif keys[pygame.K_RIGHT]:
                    self.turns[self.head.pos[:]] = [1, 0]

                elif keys[pygame.K_UP]:
                    self.turns[self.head.pos[:]] = [0, -1]

                elif keys[pygame.K_DOWN]:
                    self.turns[self.head.pos[:]] = [0, 1]

        for i,c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1,c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], rows-1)
                else: c.move(c.dirnx,c.dirny)

    def reset(self,pos,screen):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        screen.fill((0,0,0))
        label = font2.render(f'Level {level}', 1, (255, 0, 0))
        screen.blit(label, (50, 10))
        pygame.display.update()
        pygame.time.wait(1000)

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self,surface):
        for i,c in enumerate(self.body):
            if i==0:
                c.draw(surface,True)
            else:
                c.draw(surface)

def redrawWindow(surface):
    global rows, width, snake, snack, walls
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    label = font.render(f'Level {level}', 1, (255, 0, 0))
    surface.blit(label, (40, 3))
    label = font.render(f'Score {len(s.body)-1+((level-1)*(winning_score-1))}', 1, (255, 0, 0))
    surface.blit(label, (350, 3))
    for wall in walls:
        wall.draw(surface)
    pygame.display.update()

def randomSnack(rows, item, wallpos):
    position = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if (len(list(filter(lambda z:z.pos == (x,y), position))) > 0) or (x,y) in wallpos:
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost',True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def levelchk():
    global levelChk, wallpos, walls
    if level ==1:
        walls=[]
        wallpos=[]

    if level == 2:
        walls = []
        for i in range(5, 15):
            walls.append(cube((i, 15), color=(0, 0, 255)))
            walls.append(cube((i, 5), color=(0, 0, 255)))
        wallpos = []
        for wall in walls:
            wallpos.append(wall.pos)

    elif level == 3:
        walls = []
        des = [(10, 11), (10, 9), (9, 10), (9, 11), (9, 9), (11, 10), (11, 11), (11, 9), (10, 10), (12, 10), (8, 10),
               (10, 8), (10, 12)]
        for d in des:
            walls.append(cube(d, color=(0, 0, 255)))
        for i in range(5, 15):
            walls.append(cube((i, 15), color=(0, 0, 255)))
            walls.append(cube((i, 5), color=(0, 0, 255)))
        wallpos = []
        for wall in walls:
            wallpos.append(wall.pos)

    elif level == 4:
        walls = []
        for i in range(8,12):
            walls.append(cube((i,4), color=(0, 0, 255)))
            walls.append(cube((i,5), color=(0, 0, 255)))
            walls.append(cube((4,i), color=(0, 0, 255)))
            walls.append(cube((5,i), color=(0, 0, 255)))
            walls.append(cube((i, 20-6), color=(0, 0, 255)))
            walls.append(cube((i, 20-5), color=(0, 0, 255)))
            walls.append(cube((20-6, i), color=(0, 0, 255)))
            walls.append(cube((20-5, i), color=(0, 0, 255)))
        wallpos = []
        for wall in walls:
            wallpos.append(wall.pos)

    elif level == 5:
        walls = []
        for i in range(7):
            walls.append(cube((i,3), color=(0, 0, 255)))
            walls.append(cube((20-i,5), color=(0, 0, 255)))
            walls.append(cube((i,9), color=(0, 0, 255)))
            walls.append(cube((20-i,11), color=(0, 0, 255)))
            walls.append(cube((i, 15), color=(0, 0, 255)))
            walls.append(cube((20 - i, 17), color=(0, 0, 255)))
        wallpos = []
        for wall in walls:
            wallpos.append(wall.pos)

    elif level == 6:
        walls = []
        for i in range(13, 20):
            walls.append(cube((i, 13), color=(0, 0, 255)))
            walls.append(cube((13, i), color=(0, 0, 255)))
        for i in range(18, 10,-1):
            walls.append(cube((9, i+2), color=(0, 0, 255)))
            walls.append(cube((20-i,12), color=(0, 0, 255)))
        for i in range(8):
            walls.append(cube((i,5), color=(0, 0, 255)))
            walls.append(cube((20-i,5), color=(0, 0, 255)))
        wallpos = []
        for wall in walls:
            wallpos.append(wall.pos)

    snack = cube(randomSnack(rows, s, wallpos), color=(0, 255, 0))
    levelChk = False
    return snack

def main():
    global rows, width, height, s, snack, walls, level, font, font2, levelChk, winning_score
    width=500
    height=500
    rows=20
    winning_score=16
    pygame.init()
    win = pygame.display.set_mode((width,height))
    s = snake((255,0,0),(1,1))
    font = pygame.font.SysFont('monospace', 28)
    font2 = pygame.font.SysFont('monospace', 75)
    speed = 8
    flag = True
    levelChk = True
    level = 1
    clock = pygame.time.Clock()
    label = font2.render(f'Level {level}', 1, (255, 0, 0))
    win.blit(label, (50, 10))
    pygame.display.update()
    pygame.time.wait(1000)
    while flag:
        pygame.time.delay(2)
        clock.tick(speed)
        s.move()

        if levelChk == True:
            snack = levelchk()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s,wallpos), color=(0,255,0))

        if len(s.body) == winning_score and level !=6:
            levelChk = True
            if level<6:
                level += 1
            walls =[]
            redrawWindow(win)
            s.reset((1,1),win)

        for x in range(len(s.body)):
            if (s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:]))) or s.body[x].pos in wallpos:
                message_box('The Snake Died',f'You\'r score was {len(s.body)-1+(level-1)*winning_score}. Now you have been degraded to previous level')
                if level>1:
                    level -= 1
                s.reset((1,1),win)
                levelChk = True
                break
        redrawWindow(win)
main()
