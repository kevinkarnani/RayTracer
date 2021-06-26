import unittest

from features.matrix import Translation, Scaling, Matrix
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
