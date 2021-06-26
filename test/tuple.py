import unittest
import math

from features.tuple import *


class TestTuples(unittest.TestCase):
    def test_points(self):
        self.assertEqual(Tuple(4.3, -4.2, 3.1, 1.0), Point(4.3, -4.2, 3.1))

    def test_vectors(self):
        self.assertEqual(Tuple(4.3, -4.2, 3.1, 0.0), Vector(4.3, -4.2, 3.1))

    def test_addition(self):
        a = Tuple(3, -2, 5, 1)
        b = Tuple(-2, 3, 1, 0)
        self.assertEqual(a + b, Tuple(1, 1, 6, 1))

    def test_subtraction(self):
        # point - point = vector
        a = Point(3, 2, 1)
        b = Point(5, 6, 7)
        self.assertEqual(a - b, Vector(-2, -4, -6))

        # point - vector = point
        v2 = Vector(5, 6, 7)
        self.assertEqual(a - v2, Point(-2, -4, -6))

        # vector - vector = vector
        v1 = Vector(3, 2, 1)
        self.assertEqual(v1 - v2, Vector(-2, -4, -6))

    def test_negation(self):
        self.assertEqual(-Tuple(1, -2, 3, -4), Tuple(-1, 2, -3, 4))

    def test_multiplication(self):
        a = Tuple(1, -2, 3, -4)
        self.assertEqual(a * 3.5, Tuple(3.5, -7, 10.5, -14))
        self.assertEqual(0.5 * a, Tuple(0.5, -1, 1.5, -2))

    def test_division(self):
        self.assertEqual(Tuple(1, -2, 3, -4) / 2, Tuple(0.5, -1, 1.5, -2))

    def test_magnitude(self):
        self.assertEqual(Vector(1, 0, 0).magnitude(), 1)
        self.assertEqual(Vector(0, 1, 0).magnitude(), 1)
        self.assertEqual(Vector(0, 0, 1).magnitude(), 1)
        self.assertEqual(Vector(1, 2, 3).magnitude(), math.sqrt(14))
        self.assertEqual(Vector(-1, -2, -3).magnitude(), math.sqrt(14))

    def test_normalize(self):
        self.assertEqual(Vector(4, 0, 0).normalize(), Vector(1, 0, 0))
        a = Vector(1, 2, 3)
        self.assertEqual(a.normalize(), Vector(0.26726, 0.53452, 0.80178))
        self.assertEqual(a.normalize().magnitude(), 1)

    def test_dot(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)
        self.assertEqual(a.dot(b), 20)

    def test_cross(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 4)
        self.assertEqual(a.cross(b), Vector(-1, 2, -1))
        self.assertEqual(b.cross(a), Vector(1, -2, 1))
