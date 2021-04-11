from tensor import *

class Matter:
    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material

class Object:
    """A single physical object, like a box or a tree"""
    def __init__(self, pos, vel, matter, mass=None):
        """Create a new object; creating it does not add it to any scene by default"""

        self.pos: Vector = pos
        """Initial xy location of the object (this will likely change when the simulation is run)"""
        self.x = pos.x
        self.y = pos.y
        # TODO: move above to function (?)
        self.vel: Vector = vel
        """Initial xy velocity of the object"""
        # TODO: Do we need this?
        self.matter = []
        self.matter = matter
        """Matter that the object is comprised of"""

        if mass is None:
            self.mass = Scalar(1)
        elif type(mass) is Scalar:
            self.mass: Scalar = mass
            """Mass of the object"""

        # not sure if keeping this
        self.canvas = None
        self.display = None
        self.delta = Tensor([0, 0])

    def info(self):
        """Get a string representing the object's properties (mostly for debugging)"""
        return '\n'.join(str(n) for n in [self.x, self.y, self.vel])
