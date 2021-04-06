import os
import time
import random
import curses

console = curses.initscr()

class Scene:
    def __init__(self):
        self.objects = []
        self.default_char = 'o'
        self.empty = ' '
    def add(self, obj):
        self.objects.append(obj)
        return obj
    def at(self, x, y):
        return list(filter(lambda o: o.x == x and o.y == y, self.objects))
    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty
    def render(self):
        console.clear()
        console.addstr('\n'.join([''.join([self.dot(len(self.at(x, y))) for x in range(0, 20)]) for y in range(0, 20)]))

        console.refresh()
    def clear(self):
        self.objects = []
    def step(self, steps=1):
        for step in range(steps):
            for o in self.objects:
                o.x += o.vel.x
                o.y += o.vel.y

# Generic vector class
class Vec:
    def __init__(self, v=None, x=None, y=None, z=None):
        if v:
            self.x = v[0]
            self.y = v[1]
            # self.z = v[2]
        elif x and y:
            self.x = x
            self.y = y
        else:
            # print('Must provide a tuple of vector components or x and y values to initialize vector')
            self.x = 0
            self.y = 0
    def tuple(self):
        return (self.x, self.y)
    def rand(self, min, max, float=False):
        if float:
            rfunc = lambda x, y: random.uniform(x, y)
        else:
            rfunc = lambda x, y: random.randint(x, y)

        self.x = rfunc(min, max)
        self.y = rfunc(min, max)
        return self


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def info(self):
        return '\n'.join(str(n) for n in [self.x, self.y])

sim = Scene()
def random_scene():
    sim.clear()
    for i in range(20):
        x = random.randint(0, 20)
        y = random.randint(0, 20)
        sim.add(obj=Object(x, y))

random_scene()
sim.render()
time.sleep(1)
random_scene()
sim.render()
time.sleep(1)

curses.endwin()

print(sim.objects[0].info())
