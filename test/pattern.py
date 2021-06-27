import unittest

from features.matrix import Scaling, Translation, Matrix
from features.pattern import Stripe, Test, Gradient, Ring, Checker
from features.shape import Sphere
from features.tuple import Color, Point


class TestPattern(unittest.TestCase):
    def setUp(self):
        self.white = Color(1, 1, 1)
        self.black = Color(0, 0, 0)

    def test_create(self):
        pattern = Stripe(self.white, self.black)
        self.assertEqual(pattern.a, self.white)
        self.assertEqual(pattern.b, self.black)

    def test_constant_y(self):
        pattern = Stripe(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 1, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 2, 0)), self.white)

    def test_constant_z(self):
        pattern = Stripe(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 0, 1)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 0, 2)), self.white)

    def test_alternating_x(self):
        pattern = Stripe(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0.9, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(1, 0, 0)), self.black)
        self.assertEqual(pattern.color_at(Point(-0.1, 0, 0)), self.black)
        self.assertEqual(pattern.color_at(Point(-1, 0, 0)), self.black)
        self.assertEqual(pattern.color_at(Point(-1.1, 0, 0)), self.white)

    def test_obj_transformation(self):
        obj = Sphere()
        obj.set_transform(Scaling(2, 2, 2))
        pattern = Test(self.white, self.black)
        self.assertEqual(pattern.stripe_at_object(obj, Point(2, 3, 4)), Color(1, 1.5, 2))

    def test_pattern_transformation(self):
        pattern = Test(self.white, self.black)
        pattern.set_transform(Scaling(2, 2, 2))
        self.assertEqual(pattern.stripe_at_object(Sphere(), Point(2, 3, 4)), Color(1, 1.5, 2))

    def test_multiple_transformations(self):
        obj = Sphere()
        obj.set_transform(Scaling(2, 2, 2))
        pattern = Test(self.white, self.black)
        pattern.set_transform(Translation(0.5, 1, 1.5))
        self.assertEqual(pattern.stripe_at_object(obj, Point(2.5, 3, 3.5)), Color(0.75, 0.5, 0.25))

    def test_default_transformation(self):
        self.assertEqual(Test(self.white, self.black).transform, Matrix.identity(4))

    def test_set_transformation(self):
        pattern = Test(self.white, self.black)
        pattern.set_transform(Translation(1, 2, 3))
        self.assertEqual(pattern.transform, Translation(1, 2, 3))

    def test_gradient(self):
        pattern = Gradient(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0.25, 0, 0)), Color(0.75, 0.75, 0.75))
        self.assertEqual(pattern.color_at(Point(0.5, 0, 0)), Color(0.5, 0.5, 0.5))
        self.assertEqual(pattern.color_at(Point(0.75, 0, 0)), Color(0.25, 0.25, 0.25))

    def test_ring(self):
        pattern = Ring(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(1, 0, 0)), self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 1)), self.black)
        self.assertEqual(pattern.color_at(Point(0.708, 0, 0.708)), self.black)

    def test_repeat_checker_x(self):
        pattern = Checker(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0.99, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(1.01, 0, 0)), self.black)

    def test_repeat_checker_y(self):
        pattern = Checker(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 0.99, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 1.01, 0)), self.black)

    def test_repeat_checker_z(self):
        pattern = Checker(self.white, self.black)
        self.assertEqual(pattern.color_at(Point(0, 0, 0)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 0, 0.99)), self.white)
        self.assertEqual(pattern.color_at(Point(0, 0, 1.01)), self.black)
