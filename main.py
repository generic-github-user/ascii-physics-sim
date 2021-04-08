import os
import time
import random
import curses
import numpy as np

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


# TODO: add automatic unit conversions
# TODO: add physical unit reduction
# TODO: nlp interfacing

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

# TODO: numerical precision setting

class Ellipse(Shape):
    pass

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

class Name:
    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

# TODO: lighting engine?

class Appearance:
    def __init__(self):
        pass

class PhysProps:
    def __init__(self):
        pass

# TODO: diagram (auto?)
class Material:
    def __init__(self, name, abbr, elasticity, density, color='', opacity=1, ior=0, softness=1, explosiveness=0, volatility=1):
        self.name = name
        self.abbr = abbr

        self.elasticity = elasticity
        self.stiffness = self.elasticity
        self.density = density

        self.color = color
        self.opacity = opacity
        self.ior = ior

        self.softness = softness
        self.malleability = self.softness

        self.explosiveness = explosiveness
        self.volatility = volatility

class Matter:
    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material

class Unit:
    def __init__(self, name, abbr, utype):
        self.name = name
        self.abbr = abbr
        self.utype = utype

class Angle:
    def __init__(self, deg=0):
        self.deg = deg % 360
    def set(self, deg=0):
        self.deg = deg % 360

# TODO: class tree diagram
class Simulation:
    def __init__(self, world):
        self.world = world
    def group_objects(self):
        pass

class GlyphSet:
    def __init__(self, line_characters='_-\\|/', angles=[0, 0, 60, 90, 120], heights=[0, 0.5, 0.5, 0.5, 0.5]):
        self.symbols = list(zip(line_characters, angles, heights))

class Camera:
    def __init__(self, pos, zoom=1):
        self.zoom = zoom
        self.pos = pos

# TODO: modularize
# TODO: add simple shading
# TODO: add rendering noise (e.g. randomness in character selection)
class Renderer:
    def __init__(self, rtype, dims, camera, glyphs, objects):
        self.rtype = rtype
        self.dims = dims
        self.camera = camera
        self.glyphs = glyphs
        self.default_char = 'o'
        self.empty = ' '
        self.objects = objects
        self.console = curses.initscr()
    def fetch_line_glyph(self, angle, height):
        return min(self.glyphs.symbols, key=(lambda x: abs(angle - x[1]) + abs(height - x[2])))[0]
    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty
    def at(self, x, y):
        # return list(filter(lambda o: round(o.x) == x and round(o.y) == y, self.objects))
        return list(filter(lambda o: np.array_equal(np.round_(o.pos()), np.array([x, y])), self.objects))
    def build_mask(self):
        pass
    def combine_output(self, g):
        # return ['\n'.join([''.join([h for h in g])])]
        # return ['\n'.join([''.join(h.tolist()) for h in g])]
        # print(g.astype('|S1'))
        # print(g.astype(str))
        return '\n'.join([''.join(h) for h in g])
    def form_output(self, angles):
        # TODO: use numpy char array
        # char_array = np.chararray(self.dims())
        # for x, y in np.ndindex(char_array.shape):
        #     # TODO: incorporate pos
        #     char_array[x, y] = self.fetch_line_glyph(angles[x, y], 0)

        char_array = []
        dims = self.dims()
        # for x in range(dims[0]):
        #     char_array.append([self.fetch_line_glyph(angles[x, y], 0) for y in range(dims[1])])
        for x in range(dims[0]):
            row = []
            for y in range(dims[1]):
                if angles[x, y] == 0:
                    row.append(' ')
                else:
                    row.append(self.fetch_line_glyph(angles[x, y], 0.5))
            char_array.append(row)

        return char_array
    def render_frame(self, callback, steps=300, current=0, show=True, delay=0):
        con = self.console
        if show:
            con.clear()

        dims = self.dims()
        frame_angles = np.zeros(dims)
        frame_pos = np.zeros(dims)

        # TODO: separate ASCII rendering library
        # TODO: move into functions (? - not sure if this would slow program down by much)
        if self.rtype == 'point':
            output_text = '\n'.join([''.join([self.dot(len(self.at(x, y))) for x in range(0, self.dims.x)]) for y in range(0, self.dims.y)])
        elif self.rtype == 'line':
            for obj in self.objects:
                obj_geometry = obj.matter.geometry
                if type(obj_geometry) is Circle:
                    # print(True)
                    tangents = obj_geometry.get_tangents()
                    window = tangents.shape
                    xo = round(obj.pos()[0])
                    yo = round(obj.pos()[1])
                    # print(obj.pos())
                    # print(tangents)
                    # TODO: offset by half of window size
                    # TODO: fix
                    try:
                        frame_angles[xo:window[0]+xo, yo:window[1]+yo] += tangents
                    except:
                        pass

                    # should we make the angle list first?
                    output_text = self.form_output(frame_angles)
                    # print(output_text)
                    output_text = self.combine_output(output_text)
                    # print(output_text)

            if show:
                con.addstr(output_text)
                con.refresh()

        # TODO: debug mode
        # print(frame_angles)
        # TODO: add colors
        # TODO: optimize rtype
        elif self.rtype == 'canvas':
            canvas_objs = []
            for obj in self.objects:
                # draw arcs
                # TODO: fix render settings handling
                center = np.round(obj.pos()) * 10
                # TODO: use this more
                cx, cy = center
                # TODO: use actual radius
                r = 20
                coord = cx-r, cy-r, cx+r, cy+r
                # print(coord)
                # TODO: use ellipse?
                # cv_obj = myCanvas.create_arc(coord, start=0, extent=360, outline='black')
                # cv_obj = myCanvas.create_arc(coord, start=0, extent=360, outline='black', style='arc', width=5, fill='green')
                # TODO: optimize
                if not obj.display:
                    cv_obj = myCanvas.create_oval(coord)
                    obj.display = cv_obj
                    canvas_objs.append(cv_obj)
                myCanvas.move(obj.display, *obj.delta())
                # myCanvas.move(obj.display, 0.05, 0.05)
                # self.canvas.after(delay, self.move_ball)
        elif self.rtype == 'opengl':
            pass
        elif self.rtype == 'cairo':
            pass

        callback()
        if current < steps:
            root.after(33, lambda: self.render_frame(callback=callback, current=current+1, steps=300))


        # myCanvas.update()
        # myCanvas.Update()
        # TODO: use proper solution later - https://stackoverflow.com/a/21359051
        # myCanvas.update_idletasks()
        # time.sleep(delay)



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
        self.gravity_constant = Scalar(0.5)
        self.drag = 1
        self.tiny = 0.00000000001
        self.renderer = Renderer(rtype='canvas', dims=self.dims, camera=Camera(Tensor([2, 2])), glyphs=GlyphSet(), objects=self.objects)
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
                delta = o.vel() * step_length
                o.pos.n += delta
                o.delta.n = delta
                self.edge_collision(o)
                # make sure to actually call this...
                self.gravity(o)
    def randomize(self, num=20, clear=False):
        if clear:
            self.clear()
        for i in range(num):
            # rand_min = [0, 0]
            # rand_max = self.dims()
            rand_min = 10
            rand_max = 20
            r = random.randint(1, 5)
            # TODO: random func alias
            self.add(Object(pos=Tensor(np.random.uniform(rand_min, rand_max, 2)), vel=Tensor(np.random.uniform(-5, 5, [2])), matter=Matter(Circle(radius=Scalar(r)), material=None)))
        return self
    # clean all this up
    def rrender(self, callback, delay=0, steps=300):
        self.renderer.render_frame(callback, steps=steps)
        # finally! 10:26 4-7
    # def step(self):
        # self.
    # complete as adjective
    def complete_step(self, callback, steps=300):
        self.rrender(callback=callback, steps=steps)
    def simulate(self, frames=300, steps=1, delay=None, fps=30):
        if delay:
            pause = delay
        elif fps:
            pause = 1 / fps
        print(frames)
        m=0

        # phys_step = lambda: self.step(steps=steps, step_length=pause/steps)
        # root.after(round(pause * 1000), self.complete_step)
        self.complete_step(callback=self.step)

        # for frame in range(300):
            # self.render(pause)
            # for step in range(steps):

            # TODO: fix name
            # TODO: snippets
            # root.after(round(pause * 1000), self.rrender)
            # root.update_idletasks()
            # root.update()
            # myCanvas.update()
            # m+=1
            # or update canvas?
            # time.sleep(pause)
            # TODO: separate simulation and rendering loops?

        print(m)
# TODO: ALL?

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
    def __init__(self, pos, vel, matter, mass=None):
        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        # TODO: move above to function (?)
        self.vel = vel
        # TODO: Do we need this?
        self.matter = []
        self.matter = matter

        if mass is None:
            self.mass = Scalar(1)
        elif type(mass) is Scalar:
            self.mass = mass

        # not sure if keeping this
        self.canvas = myCanvas
        self.display = None
        self.delta = Tensor([0, 0])

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

# TODO: unit inference from strings
# unbtm = Material('Unobtanium', 'ubt', 1, Scalar(40, Unit('g/cm^3')))



print(Vec([50, 25]).x)
# TODO: fix dimension ordering
sim = Scene(dims=Vec([40, 45])).randomize(num=10)
# def random_scene():
#     sim.clear()
#     for i in range(10):
#         x = random.randint(0, 50)
#         y = random.randint(0, 25)
        # sim.add(obj=Object(Vec().rand(0, 30, float=True), Vec().rand(0, 0, float=True)))


# add to window and show
myCanvas.pack()
# random_scene()
sim.simulate(frames=300, fps=30)
root.mainloop()

# TODO: move this
curses.endwin()

obj = sim.objects[0]
o = sim.objects[2]

print(sim.objects[0].info())

# TODO: track total energy in system
# TODO: add gravity switch
