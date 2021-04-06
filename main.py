import os
import time
import random
import curses

console = curses.initscr()

class Scene:
    def __init__(self, dims, edge_mode='wrap'):
        self.objects = []
        self.default_char = 'o'
        self.empty = ' '
        self.units = {
            'dist': 'm',
            'time': 's'
        }
        self.dims = dims
        self.edge_mode = edge_mode
        self.gravity_constant = Scalar(0.1)
        self.drag = 1
        self.tiny = 0.00000000001
    def add(self, obj):
        self.objects.append(obj)
        return obj
    def at(self, x, y):
        return list(filter(lambda o: round(o.x) == x and round(o.y) == y, self.objects))
    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty
    def render(self, frames=1, delay=0.03):
        for frame in range(frames):
            console.clear()
            console.addstr('\n'.join([''.join([self.dot(len(self.at(x, y))) for x in range(0, self.dims.x)]) for y in range(0, self.dims.y)]))
            time.sleep(delay)
            console.refresh()
            self.step(steps=1, step_length=delay)
    def edge_collision(self, obj):
        # if obj.x > self.dims.x or obj.x < 0 or obj.y > self.dims.y or obj.y < 0:
        if self.edge_mode == 'wrap':
            obj.x = obj.x % self.dims.x
            obj.y = obj.y % self.dims.y
        elif self.edge_mode == 'bounce':
            pass
        elif self.edge_mode == 'extend':
            pass
    def clear(self):
        self.objects = []
    def step(self, steps=1, step_length=1):
        for step in range(steps):
            for o in self.objects:
                o.x += o.vel.x * step_length
                o.y += o.vel.y * step_length
                self.edge_collision(o)

class Scalar:
    def __init__(self, n=None, units=''):
        self.n = n
        self.units = units
    def root(self, n):
        return Scalar(self.n ** (1/n))

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
    def clone(self):
        # return Vec(x=self.x, y=self.y)
        return Vec(v=self.tuple())
    def abs(self):
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self
    def sub(self, b):
        self.x -= b.x
        self.y -= b.y
        return self
    def add(self, b):
        self.x += b.x
        self.y += b.y
        return self
    def each(self, f):
        return Vec(v=tuple(f(n) for n in self.tuple()))
    def square(self):
        return self.each(lambda x: x ** 2)
    def reduce(self):
        return Scalar(sum(self.tuple()))
    def info(self):
        return '\n'.join(str(n) for n in [self.x, self.y])
    def print(self):
        text = self.info()
        print(text)
        return text
    # TODO: print each in chain
    def distance(self, b):
        self.clone().sub(b).square().print()
        return self.clone().sub(b).square().reduce().root(2)

class Object:
    def __init__(self, pos, vel, mass=1):
        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        self.vel = vel
        self.mass = mass
    def info(self):
        return '\n'.join(str(n) for n in [self.x, self.y, self.vel])

sim = Scene(dims=Vec((50, 25)))
def random_scene():
    sim.clear()
    for i in range(10):
        x = random.randint(0, 50)
        y = random.randint(0, 25)
        sim.add(obj=Object(Vec().rand(0, 30, float=True), Vec().rand(-10, 10, float=True)))

random_scene()
sim.render(frames=300)

curses.endwin()

print(sim.objects[0].info())
