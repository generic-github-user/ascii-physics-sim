class Geometry:
    """Generalized multidimensional shape class"""
    def __init__(self, parts=None, dimensions=None):
        """Create a new geometry object"""

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

# 1D geometry convenience subclass
class Line(Geometry):
    def __init__(self):
        super().__init__(dimensions=1)

# 2D geometry convenience subclass
class Shape(Geometry):
    def __init__(self):
        super().__init__(dimensions=2)

# 3D geometry convenience subclass
class Solid(Geometry):
    def __init__(self):
        super().__init__(dimensions=3)

# 4D geometry convenience subclass
class Hypersolid(Geometry):
    def __init__(self):
        super().__init__(dimensions=4)



# should this subclass Geometry instead?
class Polygon(Shape):
    """General polygon class that extends the Shape class"""
    def __init__(self):
        """Create a new polygon"""
        super().__init__()
        self.sides: [line] = []
    def regular(self, sides, radius):
        """Define polygon's geometry as a regular polygon; one with equal sides and angles"""
        for s in range(sides):
            self.sides.append(Line())

# TODO: numerical precision setting

class Ellipse(Shape):
    pass

class Circle(Shape):
    """A geometric 2D circle with a certain radius; subclass of Shape"""
    def __init__(self, radius):
        super().__init__()
        self.radius: Scalar = radius
    def get_tangents(self):
        """Quickly calculate incline angle of tangent line for each cell rendered on circle outline; these will be used to render the outline in ASCII characters"""
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
