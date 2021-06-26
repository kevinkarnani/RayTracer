import unittest

from features.light import Light
from features.tuple import Point, Color


class TestLight(unittest.TestCase):
    def test_create(self):
        light = Light(Point(0, 0, 0), Color(1, 1, 1))
        self.assertEqual(light.position, Point(0, 0, 0))
        self.assertEqual(light.intensity, Color(1, 1, 1))
