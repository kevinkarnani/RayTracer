import unittest

from features.light import Light
from features.material import Material
from features.pattern import Stripe
from features.shape import Sphere
from features.tuple import Color, Vector, Point


class TestMaterial(unittest.TestCase):
    def setUp(self):
        self.m = Material()
        self.position = Point(0, 0, 0)
        self.s = Sphere()

    def test_creation(self):
        self.assertEqual(self.m.color, Color(1, 1, 1))
        self.assertEqual(self.m.ambient, 0.1)
        self.assertEqual(self.m.diffuse, 0.9)
        self.assertEqual(self.m.specular, 0.9)
        self.assertEqual(self.m.shininess, 200)

    def test_lighting_eye_between(self):
        eye_v = Vector(0, 0, -1)
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, self.position, eye_v, normal_v), Color(1.9, 1.9, 1.9))

    def test_lighting_eye_between_45(self):
        eye_v = Vector(0, (2 ** -0.5), -(2 ** -0.5))
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, self.position, eye_v, normal_v), Color(1, 1, 1))

    def test_lighting_eye_opp_45(self):
        eye_v = Vector(0, 0, -1)
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 10, -10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, self.position, eye_v, normal_v), Color(0.7364, 0.7364, 0.7364))

    def test_lighting_reflect(self):
        eye_v = Vector(0, -(2 ** -0.5), -(2 ** -0.5))
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 10, -10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, self.position, eye_v, normal_v), Color(1.6364, 1.6364, 1.6364))

    def test_lighting_behind(self):
        eye_v = Vector(0, 0, -1)
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, 10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, self.position, eye_v, normal_v), Color(0.1, 0.1, 0.1))

    def test_surface_in_shadow(self):
        eye_v = Vector(0, 0, -1)
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, self.position, eye_v, normal_v, in_shadow=True), Color(0.1, 0.1, 0.1))

    def test_lighting_with_pattern(self):
        self.m.pattern = Stripe(Color(1, 1, 1), Color(0, 0, 0))
        self.m.ambient = 1
        self.m.diffuse = 0
        self.m.specular = 0
        eye_v = Vector(0, 0, -1)
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, Point(0.9, 0, 0), eye_v, normal_v), Color(1, 1, 1))
        self.assertEqual(self.m.lighting(self.s, light, Point(1.1, 0, 0), eye_v, normal_v), Color(0, 0, 0))

    def test_default_reflective(self):
        self.assertEqual(self.m.reflective, 0)

    def test_default_transparency_refractive(self):
        self.assertEqual(self.m.transparency, 0)
        self.assertEqual(self.m.refractive_index, 1)

