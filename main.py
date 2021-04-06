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
