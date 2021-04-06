import os
import time
import random

class Scene:
    def __init__(self):
        self.objects = []
    def add(self, obj):
        self.objects.append(obj)

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def info(self):
        return '\n'.join(str(n) for n in [self.x, self.y])

sim = Scene()
for i in range(20):
    x = random.randint(0, 20)
    y = random.randint(0, 20)
    sim.add(obj=Object(x, y))

print(sim.objects[0].info())
