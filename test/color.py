import unittest

from features.tuple import Color


class TestColor(unittest.TestCase):
    def test_color(self):
        c = Color(-0.5, 0.4, 1.7)
        self.assertEqual(c.red, -0.5)
        self.assertEqual(c.green, 0.4)
        self.assertEqual(c.blue, 1.7)

    def test_addition(self):
        c1 = Color(0.9, 0.6, 0.75)
        c2 = Color(0.7, 0.1, 0.25)
        self.assertEqual(c1 + c2, Color(1.6, 0.7, 1.0))

    def test_subtraction(self):
        c1 = Color(0.9, 0.6, 0.75)
        c2 = Color(0.7, 0.1, 0.25)
        self.assertEqual(c1 - c2, Color(0.2, 0.5, 0.5))

    def test_scalar_multiplication(self):
        c = Color(0.2, 0.3, 0.4)
        self.assertEqual(c * 2, Color(0.4, 0.6, 0.8))
        self.assertEqual(0.5 * c, Color(0.1, 0.15, 0.2))

    def test_multiply_colors(self):
        c1 = Color(1, 0.2, 0.4)
        c2 = Color(0.9, 1, 0.1)
        self.assertEqual(c1 * c2, Color(0.9, 0.2, 0.04))
        self.assertEqual(c2 * c1, Color(0.9, 0.2, 0.04))
