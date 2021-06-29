import numpy as np

from features.bounds import Bounds
from features.intersection import Intersections
from features.matrix import Translation, Scaling, Rotation
from features.shape import Shape, Sphere, Cylinder


class Group(Shape):
    def __init__(self, transform=None, material=None, parent=None):
        super().__init__(transform, material, parent)
        self.shapes = []

    def add_child(self, s):
        s.parent = self
        s.material = self.material
        self.shapes.append(s)
        self.bounds()

    def local_intersect(self, ray):
        xs = Intersections()
        if not self.box:
            self.bounds()
        if self.box.intersect(ray):
            for shape in self.shapes:
                xs.extend(shape.intersect(ray))
            xs.sort()
        return xs

    def set_transform(self, t):
        super().set_transform(t)
        self.bounds()
        self.box = self.box.transform(t)

    def set_material(self, m=None):
        for shape in self.shapes:
            shape.material = self.material if m is None else m

    def bounds(self):
        box = Bounds()
        for shape in self.shapes:
            if hasattr(shape, 'minimum') or hasattr(shape, 'origin') or isinstance(shape, Group):
                shape.bounds()
                box += shape.box.transform(shape.transform)
        self.box = box


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
            edge.set_transform(Translation(0, 0, -1) * Rotation(0, -np.pi / 6) * Rotation(0, 0, -np.pi / 2)
                               * Scaling(0.25, 1, 0.25))
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
