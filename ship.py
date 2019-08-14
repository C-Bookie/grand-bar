import sys

import pygame
from pygame.locals import *

import math
import random


class Test:

	width = 800
	height = 600

	points = [
		[100, 200],
		[100, 250],
		[50, 200]
	]
	visited = []

	density = 1/100

	actors = [
		[10, 20],  # Bert
		[30, 40]   # Elma
	]

	state = 0
	step = 100

	def __init__(self):
		pygame.init()
		global surface
		surface = pygame.display.set_mode((self.width, self.height), 0, 32)
		pygame.display.set_caption("bop")

	def randP(self):
		return [random.randint(0, self.width), random.randint(0, self.height)]

	def setup(self):
		self.actors[0] = self.randP()
		self.actors[0] = self.randP()

		self.points = []
		self.visited = []
		# while random.uniform(0, 1) > self.density:
		for i in range(9):
			self.points.append(self.randP())

	def dist(self, a, b):
		return math.sqrt((abs(a[0]-b[0])**2)+(abs(a[1]-b[1])**2))

	def find_angle(self, p0,p1,c):    #credits to shaman.sir@stackoverflow
		# p0c = math.sqrt(math.pow(c[0]-p0[0],2)+ math.pow(c[1]-p0[1],2)) # p0->c (b)
		p0c = self.dist(c, p0)
		# p1c = math.sqrt(math.pow(c[0]-p1[0],2)+ math.pow(c[1]-p1[1],2)) # p1->c (a)
		p1c = self.dist(c, p1)
		# p0p1 = math.sqrt(math.pow(p1[0]-p0[0],2)+ math.pow(p1[1]-p0[1],2)) # p0->p1 (c)
		p0p1 = self.dist(p0, p1)
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

	# def flower(x, y):
	# #    return -math.sqrt(x**2+y**2)/math.cos(math.atan(y/x))
	#     return math.sqrt(x**2+y**2)*math.sqrt(y**2/x**2+1)
	#
	# def nHeart(p, a):
	#     ag = abs(find_angle(a, actors[p], actors[(p-1)%2])-180)
	#     if ag > 90:
	#         return flower()
	#     else:
	#         return math.inf

	def ground(self, n):
		return math.inf if n == 0 else n

	def score(self, p, a):
	#    ag = find_angle(a, self.actors[(p-1)%2], actors[p])
		d0 = self.dist(self.actors[p], a)
		d1 = self.dist(self.actors[(p-1)%2], a)
		d1 = self.ground(d1)
		return d0/d1

	# def score(self, p, a):
	# #    ag = find_angle(a, self.actors[(p-1)%2], actors[p])
	# 	d0 = self.dist(self.actors[p], a)
	# 	d1 = self.dist(self.actors[(p-1)%2], a)
	# 	d1 = self.ground(d1)
	# 	return (d0*d1)%1

	def move(self, p):
		choice = 0
		i = 1
		while i < len(self.points):
			if self.score(p, self.points[choice]) > self.score(p, self.points[i]):
				choice = i
			i += 1
		self.actors[p] = self.points[choice]
		if p:
			self.visited.append(self.points.pop(choice))
		else:
			self.visited.insert(0, self.points.pop(choice))

	def draw(self):
		surface.fill((32, 32, 32))

		for i, point in enumerate(self.points):
			pygame.draw.circle(surface, (128, 128, 224), (point[0], point[1]), 2)
	#        if i > 0:
	#            pygame.draw.line(surface, (128, 128, 224), (points[i-1][0], points[i-1][1]), (point[0], point[1]))

		for i, point in enumerate(self.visited):
			pygame.draw.circle(surface, (224, 128, 128), (point[0], point[1]), 2)
			if i > 0:
				pygame.draw.line(surface, (128, 224, 128), (self.visited[i-1][0], self.visited[i-1][1]), (point[0], point[1]))

		# for point in self.actors:
		pygame.draw.circle(surface, (128, 128, 224), (self.actors[0][0], self.actors[0][1]), 6)
		pygame.draw.circle(surface, (224, 128, 128), (self.actors[1][0], self.actors[1][1]), 6)

		colour = (128, 128, 224) if self.state == 0 else (224, 128, 128)

		pygame.draw.line(surface, colour, (self.actors[0][0], self.actors[0][1]), (self.actors[1][0], self.actors[1][1]))

		self.paint()

	def paint(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()

	def totalDist(self, t):
		r = 0
		for i, v in enumerate(t):
			r += self.dist(t[i-1 % len(t)], v)
		return r

	def run(self):
		while True:
			self.setup()
			self.loop()

	def loop(self):
		self.state = 0
		self.step = 500
		self.draw()
		while len(self.points) > 0:
			pygame.time.wait(self.step)
			self.move(self.state)
			self.draw()
			self.state = 0 if self.state else 1
		td = math.floor(self.totalDist(self.visited))+1
		print(str(len(self.visited)) + "\t:" + str(td) + "\t:" + str(len(self.visited)/td))
		# pygame.time.wait(self.step*10)
		pygame.time.wait(self.step*10000)

	def test(self):
		self.actors = [
			[math.floor(self.width/4), math.floor(self.height/2)],
			[math.floor(self.width/2), math.floor(self.height/2)]
		]
		scale = 2
		step = 0.01
		space = 10
		p = []

		for y in range(self.height):
			q = []
			for x in range(self.width):
				q.append(self.score(1, (x, y)))
			p.append(q)

		while True:
			scale += step
			for y in range(self.height):
				for x in range(self.width):
					surface.set_at((x, y), ((p[y][x]*space**(scale-1)) % 255, (p[y][x]*space**scale) % 255, (p[y][x]*space**(scale+1)) % 255))
			for point in self.actors:
				pygame.draw.circle(surface, (224, 224, 128), (point[0], point[1]), 2)
			self.paint()
			pygame.time.wait(100000)


if __name__ == '__main__':
	test = Test()
	test.test()
	test.run()


