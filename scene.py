import curses
import random

from tensor import *
from renderer import *
from object import *
from geometry import *

class Scene:
    """A class the brings together a world and a renderer, and provides high-level functions to facilitate their interaction"""
    def __init__(self, dims, edge_mode='wrap'):
        """Create a new scene"""

        self.objects: [Object] = []
        """A list of objects to initialize the scene with"""
        self.units = {
            'dist': 'm',
            'time': 's'
        }
        self.dims: Vector = dims
        """The width/height of the scene"""
        self.edge_mode: str = edge_mode
        """
        Defines the behavior for objects that go over the edges of the scene:
            - `wrap`: Wrap around so that an object passing through the bottom edge will come back down from the top edge, right will go to left, and so on
            - `bounce`: Bounce the object against the side of the scene as if it were a wall
            - `extend`: Let the object continue moving out of the frame
        """
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
        self.renderer.canvas.pack()

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
        self.renderer.root.mainloop()
# TODO: ALL?
