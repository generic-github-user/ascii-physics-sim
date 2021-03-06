import os
import time
import random
import curses
import numpy as np
import importlib

# modules = [
#     'scene',
#     'renderer'
# ]
# for module in modules:
#     importlib.import_module(module)

from scene import Scene
from material import Material
from object import Object
from renderer import *
from tensor import *
from geometry import *
from helpers import *

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



# TODO: add automatic unit conversions
# TODO: add physical unit reduction
# TODO: nlp interfacing
# TODO: class tree diagram
# TODO: modularize
# TODO: add simple shading
# TODO: add rendering noise (e.g. randomness in character selection)
# TODO: print each in chain
# TODO: lighting engine?
# TODO: fix dimension ordering



class Appearance:
    def __init__(self):
        pass

class PhysProps:
    def __init__(self):
        pass





class Simulation:
    """A physics simulation that processes interactions between all of a world's objects"""
    def __init__(self, world):
        """Create a new simulation"""

        self.world: World = world
        """The world that is being simulated"""
    def group_objects(self):
        pass



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
sim = Scene(dims=Vec([40, 45])).randomize(num=10)

# TODO: clean all this up

# add to window and show

# random_scene()
sim.simulate(frames=300, fps=30)


# TODO: move this
curses.endwin()

obj = sim.objects[0]
o = sim.objects[2]

print(sim.objects[0].info())

# TODO: track total energy in system
# TODO: add gravity switch
