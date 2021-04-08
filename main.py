import os
import time
import random
import curses
import numpy as np

console = curses.initscr()
# import OpenGL
# import OpenGL.GL
# import OpenGL.GLUT
# import OpenGL.GLU
#
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
#
# w,h= 500,500
# def square():
#     glBegin(GL_QUADS)
#     glVertex2f(100, 100)
#     glVertex2f(200, 100)
#     glVertex2f(200, 200)
#     glVertex2f(100, 200)
#     glEnd()
#
# def iterate():
#     glViewport(0, 0, 500, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()
#
# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#     glColor3f(1.0, 0.0, 3.0)
#     square()
#     glutSwapBuffers()
#
# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(500, 500)
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow("OpenGL Coding Practice")
# glutDisplayFunc(showScreen)
# glutIdleFunc(showScreen)
# glutMainLoop()

import tkinter


root = tkinter.Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=700, width=700)

# Generalized multidimensional shape class
class Geometry:
    def __init__(self, parts=None, dimensions=None):
        if parts:
            self.parts = parts
        else:
            self.parts = []

        if dimensions is None:
            self.dimensions = self.parts[0].dimensions + 1
        else:
            self.dimensions = dimensions


class Point(Geometry):
    def __init__(self):
        # super(Geometry, self).__init__()
        super().__init__(dimensions=0)

class Line(Geometry):
    def __init__(self):
        super().__init__(dimensions=1)

class Shape(Geometry):
    def __init__(self):
        super().__init__(dimensions=2)

class Solid(Geometry):
    def __init__(self):
        super().__init__(dimensions=3)


# should this subclass Geometry instead?
class Polygon(Shape):
    def __init__(self):
        super().__init__()
        self.sides = []
    def regular(self, sides, radius):
        for s in range(sides):
            self.sides.append(Line())

class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius
    # Quickly calculate incline angle of tangent line for each cell rendered on circle outline; these will be used to render the outline in ASCII characters
    def get_tangents(self):
        r = self.radius()
        # possibly move this code
        minigrid = np.zeros([r*2+1, r*2+1])
        # crossed_cells = minigrid
        # TODO: mirroring for efficiency?
        for x, y in np.ndindex(minigrid.shape):
            # print(5)
            # print(np.round(np.linalg.norm(np.array([x, y]) - np.array([r, r]))))
            if np.round(np.linalg.norm(np.array([x, y]) - np.array([r, r]))) == r:
                minigrid[x, y] = 1
        num_crossed = np.sum(minigrid)
        d_theta = 360 / num_crossed
        c = 0
        for x, y in np.ndindex(minigrid.shape):
            # if
            c += minigrid[x, y]
            # minigrid[x, y] = Angle(d_theta * c)
            minigrid[x, y] = d_theta * c * minigrid[x, y]
        return np.round(minigrid)

class Material:
    def __init__(self, name, elasticity, density):
        self.name = name
        self.elasticity = elasticity
        self.density = density

class Matter:
    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material

class Unit:
    def __init__(self, name, abbr, utype):
        self.name = name
        self.abbr = abbr
        self.utype = utype

# TODO: class tree diagram
class Simulation:
    def __init__(self):
        pass

class GlyphSet:
    def __init__(self, line_characters='_-\\|/', angles=[0, 0, 60, 90, 120], heights=[0, 0.5, 0.5, 0.5, 0.5]):
        self.symbols = zip(line_characters, angles, heights)

class Camera:
    def __init__(self, pos, zoom=1):
        self.zoom = zoom
        self.pos = pos

# TODO: add simple shading
class Renderer:
    def __init__(self, rtype, dims, camera, glyphs, objects):
        self.rtype = rtype
        self.dims = dims
        self.camera = camera
        self.glyphs = glyphs
        self.default_char = 'o'
        self.empty = ' '
        self.objects = objects
    def fetch_line_glyph(self, angle, height):
        return min(self.glyphs, key=lambda x: abs(angle - x[1]) + abs(height - x[2]))[0]
    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty
    def at(self, x, y):
        # return list(filter(lambda o: round(o.x) == x and round(o.y) == y, self.objects))
        return list(filter(lambda o: np.array_equal(np.round_(o.pos()), np.array([x, y])), self.objects))
    def render_frame(self):
        console.clear()
        console.addstr('\n'.join([''.join([self.dot(len(self.at(x, y))) for x in range(0, self.dims.x)]) for y in range(0, self.dims.y)]))
        console.refresh()
        # TODO: optimization
        # TODO: per-shape and per-cell rendering

class Scene:
    def __init__(self, dims, edge_mode='wrap'):
        self.objects = []
        self.units = {
            'dist': 'm',
            'time': 's'
        }
        self.dims = dims
        self.edge_mode = edge_mode
        self.gravity_constant = Scalar(10)
        self.drag = 1
        self.tiny = 0.00000000001
        self.renderer = Renderer('line', self.dims, Camera(Tensor([2, 2])), GlyphSet(), self.objects)
    def add(self, obj):
        self.objects.append(obj)
        return obj
    def edge_collision(self, obj):
        # if obj.x > self.dims.x or obj.x < 0 or obj.y > self.dims.y or obj.y < 0:
        if self.edge_mode == 'wrap':
            # obj.x = obj.x % self.dims.x
            # obj.y = obj.y % self.dims.y
            obj.pos.n = obj.pos() % self.dims()
        elif self.edge_mode == 'bounce':
            pass
        elif self.edge_mode == 'extend':
            pass
    def gravity(self, obj):
        for o in self.objects:
            if obj is not o:
                dist = obj.pos.distance(o.pos)
                if dist == 0:
                    dist = self.tiny

                # wrap distance?
                # use unit vector or use original vector directly in equation?
                # obj.pos.n += (self.gravity_constant() * obj.mass() * o.mass() / (dist ** 2)) / obj.mass()
                obj.vel.n += (self.gravity_constant() * obj.mass() * o.mass() / (dist ** 2)) / obj.mass() * (o.pos()-obj.pos())
                # print(obj.vel.n)
        # for o in self.objects:
        #     dist = obj.pos.distance2(o.pos)
        #     if dist == 0:
        #         dist = self.tiny
            # obj.vel.x += (self.gravity_constant * obj.mass * o.mass / (dist ** 2)) / obj.mass
            # TODO: address mutability
            # TODO: mass 1 should cancel out
            # obj.vel.add(self.gravity_constant.mul(obj.mass).mul(o.mass).div(dist.square())).div(obj.mass)
    def clear(self):
        self.objects = []
    def step(self, steps=1, step_length=1):
        for step in range(steps):
            for o in self.objects:
                # TODO: cache position, velocity, etc. before applying physics step
                # TODO: collect list of forces acting on object
                # TODO: replace this with vector operation
                # o.x += o.vel.x * step_length
                # o.y += o.vel.y * step_length
                o.pos.n += o.vel() * step_length
                self.edge_collision(o)
                # make sure to actually call this...
                self.gravity(o)
    def randomize(self, num=20):
        for i in range(num):
            # rand_min = [0, 0]
            # rand_max = self.dims()
            rand_min = 0
            rand_max = 30
            self.add(Object(pos=Tensor(np.random.uniform(rand_min, rand_max, 2)), vel=Tensor(np.zeros(2))))
        return self
    # clean all this up
    def render(self):
        self.renderer.render_frame()
    # def step(self):
    #     self.
    def simulate(self, frames=30, steps=1, delay=None, fps=30):
        if delay:
            pause = delay
        elif fps:
            pause = 1 / fps

        for frame in range(frames):
            self.render()
            # for step in range(steps):
            self.step(steps=steps, step_length=pause/steps)
            # time.sleep(pause)
            # TODO: separate simulation and rendering loops?

class Tensor:
    def __init__(self, n, units=''):
        self.n = np.array(n)
        self.forces = []
        self.units = units
        if self.n.size == 2:
            self.x = self.n[0]
            self.y = self.n[1]
    # def __repr__(self):
    def __call__(self):
        return self.n
    # TODO: optimize distance-finding in gravity algorithm
    def distance(self, b):
        return np.linalg.norm(self.n-b.n)

Scalar = Tensor
Vector = Tensor
Vec = Tensor

# TODO: generalize
# class Scalar:
#     def __init__(self, n, units=''):
#         self.n = n
#         self.units = units
#     def __repr__(self):
#         return self.n
#     # reuse vector operations (?)
#     def op(self, b, f):
#         m = self.n
#         if type(b) is Vec:
#             return Vec((f(m, b.x), f(m, b.y)))
#         elif type(b) is Scalar:
#             self.n = f(self.n, b.n)

# Generic vector class
# class Vec:
#     def __init__(self, v=None, x=None, y=None, z=None, units=''):
#         if v:
#             self.x = v[0]
#             self.y = v[1]
#             # self.z = v[2]
#         elif x and y:
#             self.x = x
#             self.y = y
#         else:
#             # print('Must provide a tuple of vector components or x and y values to initialize vector')
#             self.x = 0
#             self.y = 0
#     # generate tuple automatically?
#     def tuple(self):
#         return (self.x, self.y)
#     def rand(self, min, max, float=False):
#         if float:
#             rfunc = lambda x, y: random.uniform(x, y)
#         else:
#             rfunc = lambda x, y: random.randint(x, y)
#
#         self.x = rfunc(min, max)
#         self.y = rfunc(min, max)
#         return self
#     def clone(self):
#         # return Vec(x=self.x, y=self.y)
#         return Vec(v=self.tuple())
#     def op(self, b, f):
#         if type(b) is Vec:
#             self.x = f(self.x, b.x)
#             self.y = f(self.y, b.y)
#         elif type(b) is Scalar:
#             self.x = f(self.x, b.n)
#             self.y = f(self.y, b.n)
#     def each(self, f):
#         return Vec(v=tuple(f(n) for n in self.tuple()))
#     def square(self):
#         return self.each(lambda x: x ** 2)
#     def reduce(self):
#         return Scalar(sum(self.tuple()))
#     def info(self):
#         return '\n'.join(str(n) for n in [self.x, self.y])
#     def print(self):
#         text = self.info()
#         print(text)
#         return text
#     # TODO: print each in chain
#     def distance(self, b):
#         # self.clone().sub(b).square().print()
#         return self.clone().sub(b).square().reduce().root(2)
#     def distance2(self, b):
#         return self.clone().sub(b).square().root(2)

class Object:
    def __init__(self, pos, vel, mass=None):
        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        # TODO: move above to function (?)
        self.vel = vel
        self.matter = []
        if mass is None:
            self.mass = Scalar(1)
        elif type(mass) is Scalar:
            self.mass = mass
    def info(self):
        return '\n'.join(str(n) for n in [self.x, self.y, self.vel])

class Cluster:
    def __init__(self):
        self.objects = []

class World:
    def __init__(self, dims):
        self.stuff = []
        self.dims = dims
    def snap():
        self.stuff = []

class Universe:
    pass

print(Vec([50, 25]).x)
sim = Scene(dims=Vec([50, 25])).randomize(num=10)
# def random_scene():
#     sim.clear()
#     for i in range(10):
#         x = random.randint(0, 50)
#         y = random.randint(0, 25)
        # sim.add(obj=Object(Vec().rand(0, 30, float=True), Vec().rand(0, 0, float=True)))

# random_scene()
sim.simulate(frames=30, fps=30)

# TODO: move this
curses.endwin()

# print(sim.objects[0].info())
# print(Vec((0, 0)).distance(Vec((3, 4))).n)
obj = sim.objects[0]
o = sim.objects[2]
# print(obj.pos.distance(o.pos).n ** 2)
# print((1000 * obj.mass * o.mass / (obj.pos.distance(o.pos).n ** 2)) / obj.mass)
# print(sim.dims())
# print(obj.pos())
# print(o.pos())
# print(obj.pos.distance(o.pos))
# print((1000 * obj.mass() * o.mass() / ((obj.pos.distance(o.pos)+0.000000001) ** 2)) / obj.mass())

print(sim.objects[0].info())

# TODO: track total energy in system
# TODO: add gravity switch
