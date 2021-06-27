import unittest

from features.intersection import Intersection, Intersections
from features.matrix import Translation, Scaling
from features.ray import Ray
from features.shape import Sphere, Plane
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

    def test_hit_over_offset(self):
        s = Sphere()
        s.set_transform(Translation(0, 0, 1))
        comps = Intersection(5, s).prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertLess(comps.over_point.z, -0.00001 / 2)
        self.assertGreater(comps.point.z, comps.over_point.z)

    def test_precomputing_reflection(self):
        self.assertEqual(Intersection((2 ** 0.5), Plane()).prepare_computations(
            Ray(Point(0, 1, -1), Vector(0, -(2 ** -0.5), (2 ** -0.5)))).reflect_v, Vector(0, (2 ** -0.5), (2 ** -0.5)))

    def test_finding_normal_refractive(self):
        a = Sphere.glassy()
        a.set_transform(Scaling(2, 2, 2))
        b = Sphere.glassy()
        b.material.refractive_index = 2
        b.set_transform(Translation(0, 0, -0.25))
        c = Sphere.glassy()
        c.material.refractive_index = 2.5
        c.set_transform(Translation(0, 0, 0.25))
        xs = Intersections(Intersection(2, a), Intersection(2.75, b), Intersection(3.25, c), Intersection(4.75, b),
                           Intersection(5.25, c), Intersection(6, a))

        xs = [i.prepare_computations(Ray(Point(0, 0, -4), Vector(0, 0, 1)), xs) for i in xs]
        self.assertEqual(xs[0].n1, 1.0)
        self.assertEqual(xs[0].n2, 1.5)
        self.assertEqual(xs[1].n1, 1.5)
        self.assertEqual(xs[1].n2, 2.0)
        self.assertEqual(xs[2].n1, 2.0)
        self.assertEqual(xs[2].n2, 2.5)
        self.assertEqual(xs[3].n1, 2.5)
        self.assertEqual(xs[3].n2, 2.5)
        self.assertEqual(xs[4].n1, 2.5)
        self.assertEqual(xs[4].n2, 1.5)
        self.assertEqual(xs[5].n1, 1.5)
        self.assertEqual(xs[5].n2, 1.0)

    def test_hit_under_offset(self):
        s = Sphere.glassy()
        s.set_transform(Translation(0, 0, 1))
        i = Intersection(5, s)
        comps = i.prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1)), Intersections(i))
        self.assertGreater(comps.under_point.z, 0.00001 / 2)
        self.assertLess(comps.point.z, comps.under_point.z)

    def test_schlick_total_reflection(self):
        s = Sphere.glassy()
        xs = Intersections(Intersection(-(2 ** -0.5), s), Intersection(2 ** -0.5, s))
        comps = xs[1].prepare_computations(Ray(Point(0, 0, 2 ** -0.5), Vector(0, 1, 0)), xs)
        self.assertEqual(comps.schlick(), 1.0)

    def test_schlick_perpendicular(self):
        s = Sphere.glassy()
        xs = Intersections(Intersection(-1, s), Intersection(1, s))
        comps = xs[1].prepare_computations(Ray(Point(0, 0, 0), Vector(0, 1, 0)), xs)
        self.assertAlmostEqual(comps.schlick(), 0.04)

    def test_schlick_small_angle(self):
        s = Sphere.glassy()
        xs = Intersections(Intersection(1.8589, s))
        comps = xs[0].prepare_computations(Ray(Point(0, 0.99, -2), Vector(0, 0, 1)), xs)
        self.assertAlmostEqual(comps.schlick(), 0.48873, places=5)
