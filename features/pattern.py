import numpy as np

from features.matrix import Matrix
from features.tuple import Color


class Pattern:
    def __init__(self, a, b, transform=None):
        self.a = a
        self.b = b
        self.transform = Matrix.identity(4) if not transform else transform

    def set_transform(self, t):
        self.transform = t

    def color_at(self, point):
        pass

    def stripe_at_object(self, obj, world_point):
        return self.color_at(self.transform.inverse() * obj.transform.inverse() * world_point)


class Test(Pattern):
    def __init__(self, a, b, transform=None):
        super().__init__(a, b, transform)

    def color_at(self, point):
        return Color(point.x, point.y, point.z)


class Stripe(Pattern):
    def __init__(self, a, b, transform=None):
        super().__init__(a, b, transform)

    def color_at(self, point):
        return self.a if np.floor(point.x) % 2 == 0 else self.b


class Gradient(Pattern):
    def __init__(self, a, b, transform=None):
        super().__init__(a, b, transform)

    def color_at(self, point):
        return self.a + (self.b - self.a) * (point.x - np.floor(point.x))


class Ring(Pattern):
    def __init__(self, a, b, transform=None):
        super().__init__(a, b, transform)

    def color_at(self, point):
        return self.a if np.floor(np.sqrt(point.x ** 2 + point.z ** 2)) % 2 == 0 else self.b


class Checker(Pattern):
    def __init__(self, a, b, transform=None):
        super().__init__(a, b, transform)

    def color_at(self, point):
        return self.a if (np.floor(point.x) + np.floor(point.y) + np.floor(point.z)) % 2 == 0 else self.b
