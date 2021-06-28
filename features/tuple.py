import numpy as np


class Tuple:
    """
    Class for holding points and vectors. Vectors denoted by w = 0, Points denoted by w = 1.
    """

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        return abs(self.x - other.x) < 0.0001 and abs(self.y - other.y) < 0.0001 and abs(
            self.z - other.z) < 0.0001 and self.w == other.w

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z and self.w == other.w

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.z >= other.z and self.w == other.w

    def __add__(self, other):
        if self.w + other.w in [0, 1]:
            return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        else:
            print("Cannot add two points together!")

    def __sub__(self, other):
        if self.w - other.w in [0, 1]:
            return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
        else:
            print("Cannot subtract a point from a vector!")

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__(self.x * other, self.y * other, self.z * other, self.w * other)
        else:
            print("Cannot multiply tuple by anything apart from int and float!")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__(self.x / other, self.y / other, self.z / other, self.w / other)
        else:
            print("Cannot divide tuple by anything apart from int and float!")

    def magnitude(self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)

    def normalize(self):
        length = self.magnitude()
        return self.__class__(self.x / length, self.y / length, self.z / length,
                              self.w / length) if length else self.__class__(0, 0, 0, 0)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def cross(self, other):
        return self.__class__(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                              self.x * other.y - self.y * other.x, self.w)

    def reflect(self, normal):
        return self - normal * 2 * self.dot(normal)

    def __str__(self):
        return f"x: {self.x} , y: {self.y}, z: {self.z}, w: {self.w}"


class Point(Tuple):
    def __init__(self, x, y, z, w=1):
        super().__init__(x, y, z, w)

    def __str__(self) -> str:
        return f"P({self.x}, {self.y}, {self.z})"


class Vector(Tuple):
    def __init__(self, x, y, z, w=0):
        super().__init__(x, y, z, w)

    def __str__(self):
        return f"V({self.x}, {self.y}, {self.z})"


class Color(Tuple):
    def __init__(self, r, g, b, w=0):
        super().__init__(r, g, b, w)

    @property
    def red(self):
        return self.x

    @property
    def green(self):
        return self.y

    @property
    def blue(self):
        return self.z

    def __mul__(self, other):
        if isinstance(other, Color):
            return Color(self.red * other.red, self.green * other.green, self.blue * other.blue)
        return super().__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f"C({self.red}, {self.green}, {self.blue})"

    def to_rgb(self):
        r = int(np.ceil(max(min(255, 255 * self.red), 0)))
        g = int(np.ceil(max(min(255, 255 * self.green), 0)))
        b = int(np.ceil(max(min(255, 255 * self.blue), 0)))
        return r, g, b
