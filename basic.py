import sys

import pygame
from pygame.locals import *

import math
import random

width = 400
height = 300

points = [
    [100, 200],
    [100, 250],
    [50, 200]
]
visited = []

density = 1/100

actors = [
    [10, 20], #Bert
    [30, 40]  #Elma
]

def init():
    pygame.init()
    global surface
    surface = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("bop")

def randP():
    return [random.randint(0, width), random.randint(0, height)]

def setup():
    global actors
    global points
    global visited

    actors[0] = randP()
    actors[0] = randP()

    points = []
    visited = []
    while random.uniform(0, 1) > density:
        points.append(randP())

def dist(a, b):
    return math.sqrt((abs(a[0]-b[0])**2)+(abs(a[1]-b[1])**2))

def find_angle(p0,p1,c):    #credits to shaman.sir@stackoverflow
    p0c = math.sqrt(math.pow(c[0]-p0[0],2)+ math.pow(c[1]-p0[1],2)) # p0->c (b)
    p0c = dist(c, p0)
    p1c = math.sqrt(math.pow(c[0]-p1[0],2)+ math.pow(c[1]-p1[1],2)) # p1->c (a)
    p1c = dist(c, p1)
    p0p1 = math.sqrt(math.pow(p1[0]-p0[0],2)+ math.pow(p1[1]-p0[1],2)) # p0->p1 (c)
    p0p1 = dist(p0, p1)
    m = (2*p1c*p0c)
    if m == 0:
        return 0
    temp = (p1c*p1c+p0c*p0c-p0p1*p0p1)/m
    if temp < -1:
        temp = -1
    elif temp > 1:
        temp = 1
    r = math.acos(temp)
    return 180*(r/math.pi)

def flower(x, y):
#    return -math.sqrt(x**2+y**2)/math.cos(math.atan(y/x))
    return math.sqrt(x**2+y**2)*math.sqrt(y**2/x**2+1)

def nHeart(p, a):
    ag = abs(find_angle(a, actors[p], actors[(p-1)%2])-180)
    if ag > 90:
        return flower()
    else:
        return math.inf



def score(p, a):
    ag = find_angle(a, actors[(p-1)%2], actors[p])
    d0 = dist(actors[p], a)
    d1 = dist(actors[(p-1)%2], a)
    return d0*-d1
#    return d*(180-ag)
    if ag == 0:
        return 0
    return ag**2

def move(p):
    choice = 0
    i = 1
    while i < len(points):
        if score(p, points[choice]) > score(p, points[i]):
            choice = i
        i+=1
    actors[p] = points[choice]
    if p:
        visited.append(points.pop(choice))
    else:
        visited.insert(0, points.pop(choice))

def draw():
    surface.fill((32, 32, 32))

    for i, point in enumerate(points):
        pygame.draw.circle(surface, (128, 128, 224), (point[0], point[1]), 2)
#        if i > 0:
#            pygame.draw.line(surface, (128, 128, 224), (points[i-1][0], points[i-1][1]), (point[0], point[1]))

    for i, point in enumerate(visited):
        pygame.draw.circle(surface, (224, 128, 128), (point[0], point[1]), 2)
        if i > 0:
            pygame.draw.line(surface, (224, 128, 128), (visited[i-1][0], visited[i-1][1]), (point[0], point[1]))

    for point in actors:
        pygame.draw.circle(surface, (224, 224, 128), (point[0], point[1]), 2)

    pygame.draw.line(surface, (128, 224, 128), (actors[0][0], actors[0][1]), (actors[1][0], actors[1][1]))

    paint()

def paint():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

def totalDist(t):
    r = 0
    for i, v in enumerate(t):
        r+=dist(t[i-1%len(t)], v)
    return r

def run():
    state = 0
    step = 100
    draw()
    while len(points) > 0:
        pygame.time.wait(step)
        move(state)
        draw()
        state = 0 if state else 1
    td = math.floor(totalDist(visited))+1
    print(str(len(visited))+"\t:"+str(td)+"\t:"+str(len(visited)/td))
    pygame.time.wait(step*10)


def test():
    global actors
    actors = [
        [math.floor(width/4), math.floor(height/2)],
        [math.floor(width/2), math.floor(height/2)]
    ]
    scale = -1
    step = 0.01
    space = 10
    p=[]

    for y in range(height):
        q=[]
        for x in range(width):
            q.append(score(1, (x, y)))
        p.append(q)

    while True:
        scale+=step
        for y in range(height):
            for x in range(width):
                surface.set_at((x, y), ((p[y][x]*space**(scale-1))%255, (p[y][x]*space**(scale))%255, (p[y][x]*space**(scale+1))%255))
        for point in actors:
            pygame.draw.circle(surface, (224, 224, 128), (point[0], point[1]), 2)
        paint()
#        pygame.time.wait(100)


if __name__ == '__main__':
    init()
    test()
    while True:
        setup()
        run()



