import numpy as np

from features.bounds import Bounds
from features.intersection import Intersections
from features.matrix import Translation, Scaling, Rotation
from features.shape import Shape, Sphere, Cylinder
from features.tuple import Point


class Group(Shape):
    def __init__(self, transform=None, material=None, parent=None):
        super().__init__(transform, material, parent)
        self.shapes = []

    def add_child(self, s):
        s.parent = self
        self.shapes.append(s)

    def local_intersect(self, ray):
        xs = Intersections()
        if not self.box:
            self.bounds()
        if self.box.intersect(ray):
            for shape in self.shapes:
                xs.extend(shape.intersect(ray))
            xs.sort()
        return xs

    def bounds(self):
        x_min, y_min, z_min = -float('inf'), -float('inf'), -float('inf')
        x_max, y_max, z_max = float('inf'), float('inf'), float('inf')

        for shape in self.shapes:
            shape.bounds()
            bound = shape.box.transform(shape.transform)
            if bound.maximum.x > x_max:
                x_max = bound.maximum.x
            if bound.maximum.y > y_max:
                y_max = bound.maximum.y
            if bound.maximum.z > z_max:
                z_max = bound.maximum.z
            if bound.minimum.x > x_min:
                x_min = bound.minimum.x
            if bound.maximum.y > y_min:
                y_min = bound.minimum.y
            if bound.minimum.z > z_min:
                z_min = bound.minimum.z

        self.box = Bounds(minimum=Point(x_min, y_min, z_min), maximum=Point(x_max, y_max, z_max))


class Hexagon(Group):
    def __init__(self, transform=None, material=None, parent=None):
        super().__init__(transform, material, parent)

    def create(self):
        def create_corner():
            corner = Sphere()
            corner.set_transform(Translation(0, 0, -1) * Scaling(0.25, 0.25, 0.25))
            return corner

        def create_edge():
            edge = Cylinder(minimum=0, maximum=1)
            edge.set_transform(Translation(0, 0, -1) * Rotation(0, -np.pi / 6, -np.pi / 2) * Scaling(0.25, 1, 0.25))
            return edge

        def create_side():
            side = Group()
            side.add_child(create_corner())
            side.add_child(create_edge())
            return side

        for n in range(6):
            side = create_side()
            side.set_transform(Rotation(0, n * np.pi / 3, 0))
            self.add_child(side)
        return self
