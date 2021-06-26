import unittest

import numpy as np

from features.material import Material
from features.matrix import Translation, Scaling, Matrix, Rotation
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Point, Vector


class TestShape(unittest.TestCase):
    def test_ray_intersects_twice(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 1)
        self.assertEqual(xs, [4, 6])

    def test_ray_intersects_once(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 1)
        self.assertEqual(xs, [5, 5])

    def test_ray_never_intersects(self):
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 0)
        self.assertEqual(xs, [])

    def test_ray_origin_inside_sphere(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 1)
        self.assertEqual(xs, [-1, 1])

    def test_sphere_behind_ray(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 1)
        self.assertEqual(xs, [-6, -4])

    def test_intersect_sets_object(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 1)
        self.assertEqual(xs.obj, s)

    def test_sphere_default_transformation(self):
        s = Sphere()
        self.assertEqual(s.transform, Matrix.identity(4))

    def test_changing_sphere_transformation(self):
        s = Sphere()
        t = Translation(2, 3, 4)
        s.set_transform(t)
        self.assertEqual(s.transform, t)

    def test_intersecting_scaled_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.set_transform(Scaling(2, 2, 2))
        xs = s.intersect(r)
        self.assertEqual(xs.count, 1)
        self.assertEqual(xs, [3, 7])

    def test_intersecting_translated_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.set_transform(Translation(5, 0, 0))
        xs = s.intersect(r)
        self.assertEqual(xs.count, 0)

    def test_normal_x(self):
        self.assertEqual(Sphere().normal_at(Point(1, 0, 0)), Vector(1, 0, 0))

    def test_normal_y(self):
        self.assertEqual(Sphere().normal_at(Point(0, 1, 0)), Vector(0, 1, 0))

    def test_normal_z(self):
        self.assertEqual(Sphere().normal_at(Point(0, 0, 1)), Vector(0, 0, 1))

    def test_nonaxial_normal(self):
        a = 3 ** 0.5 / 3
        self.assertEqual(Sphere().normal_at(Point(a, a, a)), Vector(a, a, a))

    def test_normal_is_normalized(self):
        s = Sphere()
        a = 3 ** 0.5 / 3
        n = s.normal_at(Point(a, a, a))
        self.assertEqual(n, n.normalize())

    def test_translated_normal(self):
        s = Sphere()
        s.set_transform(Translation(0, 1, 0))
        self.assertEqual(s.normal_at(Point(0, 1.70711, -0.70711)), Vector(0, 0.70711, -0.70711))

    def test_transformed_normal(self):
        s = Sphere()
        s.set_transform(Scaling(1, 0.5, 1) * Rotation(0, 0, np.pi / 5))
        self.assertEqual(s.normal_at(Point(0, 2 ** -0.5, -(2 ** -0.5))), Vector(0, 0.97014, -0.24254))

    def test_def_material(self):
        s = Sphere()
        self.assertEqual(s.material, Material())

    def test_assign_material(self):
        s = Sphere(material=Material(ambient=1))
        self.assertEqual(s.material, Material(ambient=1))
        self.assertEqual(s.material.ambient, 1)
