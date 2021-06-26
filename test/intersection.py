import unittest

from features.intersection import Intersection, Intersections
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Point, Vector


class TestIntersection(unittest.TestCase):
    def test_creation(self):
        i = Intersection(3.5, Sphere())
        self.assertEqual(i.t, 3.5)
        self.assertEqual(i.obj, Sphere())

    def test_aggregration(self):
        xs = Intersections(Intersection(1, Sphere()), Intersection(2, Sphere()))
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[1].t, 2)

    def test_all_pos(self):
        i1 = Intersection(1, Sphere())
        i2 = Intersection(2, Sphere())
        self.assertEqual(Intersections(i2, i1).hit(), i1)

    def test_mixed(self):
        i1 = Intersection(-1, Sphere())
        i2 = Intersection(1, Sphere())
        self.assertEqual(Intersections(i2, i1).hit(), i2)

    def test_all_neg(self):
        self.assertIsNone(Intersections(Intersection(-1, Sphere()), Intersection(-2, Sphere())).hit())

    def test_lowest_pos(self):
        s = Sphere()
        i1 = Intersection(5, s)
        i2 = Intersection(7, s)
        i3 = Intersection(-3, s)
        i4 = Intersection(2, s)
        self.assertEqual(Intersections(i1, i2, i3, i4).hit(), i4)

    def test_precomputing(self):
        comps = Intersection(4, Sphere()).prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(comps.t, 4)
        self.assertEqual(comps.obj, Sphere())
        self.assertEqual(comps.point, Point(0, 0, -1))
        self.assertEqual(comps.eye_v, Vector(0, 0, -1))
        self.assertEqual(comps.normal_v, Vector(0, 0, -1))

    def test_hit_out(self):
        comps = Intersection(4, Sphere()).prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertFalse(comps.inside)

    def test_hit_in(self):
        comps = Intersection(1, Sphere()).prepare_computations(Ray(Point(0, 0, 0), Vector(0, 0, 1)))
        self.assertEqual(comps.point, Point(0, 0, 1))
        self.assertEqual(comps.eye_v, Vector(0, 0, -1))
        self.assertTrue(comps.inside)
        self.assertEqual(comps.normal_v, Vector(0, 0, -1))
