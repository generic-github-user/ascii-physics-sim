import numpy as np

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

# TODO: dimensions property

# class Scalar(Tensor):
#     def __init__(self, n):
#         super().__init__(n)
#
# class Vector(Tensor):
#     def __init__(self, n):
#         super().__init__(n)
#
# class Vec(Tensor):
#     def __init__(self, n):
#         super().__init__(n)
