import unittest

import numpy as np

from features.bounds import Bounds
from features.group import Group
from features.matrix import Matrix, Translation, Scaling, Rotation
from features.ray import Ray
from features.shape import Test, Sphere, Cylinder
from features.tuple import Vector, Point


class TestGroup(unittest.TestCase):
    def test_creation(self):
        self.assertEqual(Group().transform, Matrix.identity(4))
        self.assertEqual(Group().shapes, [])

    def test_add_child(self):
        g = Group()
        t = Test()
        g.add_child(t)
        self.assertEqual(g.shapes[0], t)
        self.assertEqual(t.parent, g)

    def test_ray_intersect_empty(self):
        g = Group()
        self.assertEqual(g.intersect(Ray(Point(0, 0, 0), Vector(0, 0, 1))), [])

    def test_ray_intersect_filled(self):
        g = Group()
        s1 = Sphere()
        s2 = Sphere()
        s2.set_transform(Translation(0, 0, -3))
        s3 = Sphere()
        s3.set_transform(Translation(5, 0, 0))
        g.add_child(s1)
        g.add_child(s2)
        g.add_child(s3)
        xs = g.intersect(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(xs.count, 4)
        self.assertEqual(xs[0].obj, s2)
        self.assertEqual(xs[1].obj, s2)
        self.assertEqual(xs[2].obj, s1)
        self.assertEqual(xs[3].obj, s1)

    def test_transform(self):
        g = Group()
        g.set_transform(Scaling(2, 2, 2))
        s = Sphere()
        s.set_transform(Translation(5, 0, 0))
        g.add_child(s)
        self.assertEqual(g.intersect(Ray(Point(10, 0, -10), Vector(0, 0, 1))).count, 2)

    def test_world_to_obj(self):
        g1 = Group()
        g1.set_transform(Rotation(0, np.pi / 2, 0))
        g2 = Group()
        g2.set_transform(Scaling(2, 2, 2))
        g1.add_child(g2)
        s = Sphere()
        s.set_transform(Translation(5, 0, 0))
        g2.add_child(s)
        self.assertEqual(s.world_to_object(Point(-2, 0, -10)), Point(0, 0, -1))

    def test_normal_to_world(self):
        g1 = Group()
        g1.set_transform(Rotation(0, np.pi / 2, 0))
        g2 = Group()
        g2.set_transform(Scaling(1, 2, 3))
        g1.add_child(g2)
        s = Sphere()
        s.set_transform(Translation(5, 0, 0))
        g2.add_child(s)
        self.assertEqual(s.normal_to_world(Vector(3 ** -0.5, 3 ** -0.5, 3 ** -0.5)), Vector(0.2857, 0.4286, -0.8571))

    def test_normal_on_child(self):
        g1 = Group()
        g1.set_transform(Rotation(0, np.pi / 2, 0))
        g2 = Group()
        g2.set_transform(Scaling(1, 2, 3))
        g1.add_child(g2)
        s = Sphere()
        s.set_transform(Translation(5, 0, 0))
        g2.add_child(s)
        self.assertEqual(s.normal_at(Point(1.7321, 1.1547, -5.5774)), Vector(0.2857, 0.4286, -0.8571))

    def test_bounds_on_group(self):
        g = Group()
        self.assertIsNone(g.box)
        g.add_child(Sphere())
        self.assertEqual(g.box, Bounds(Point(-1, -1, -1), Point(1, 1, 1)))
        g.add_child(Cylinder(minimum=1, maximum=2))
        self.assertEqual(g.box, Bounds(Point(-1, -1, -1), Point(1, 2, 1)))
        g.set_transform(Scaling(2, 10, 2))
        self.assertEqual(g.box, Bounds(Point(-2, -10, -2), Point(2, 20, 2)))
