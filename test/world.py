import unittest

from features.intersection import Intersection
from features.light import Light
from features.material import Material
from features.matrix import Scaling
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Point, Color, Vector
from features.world import World


class TestWorld(unittest.TestCase):
    def test_creation(self):
        w = World()
        self.assertIsNone(w.light)
        self.assertEqual(w.objects, [])

    def test_default(self):
        w = World.default()
        s1, s2 = Sphere(), Sphere()
        s1.material = Material(color=Color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2)
        s2.set_transform(Scaling(0.5, 0.5, 0.5))
        self.assertEqual(w.light, Light(Point(-10, 10, -10), Color(1, 1, 1)))
        self.assertIn(s1, w.objects)
        self.assertIn(s2, w.objects)

    def test_intersect(self):
        w = World.default()
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        intersections = w.intersect(r)
        self.assertEqual(len(intersections), 4)
        self.assertEqual(intersections[0].t, 4)
        self.assertEqual(intersections[1].t, 4.5)
        self.assertEqual(intersections[2].t, 5.5)
        self.assertEqual(intersections[3].t, 6)

    def test_shading(self):
        w = World.default()
        c = w.shade_hit(Intersection(4, w.objects[0]).prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1))))
        self.assertEqual(c, Color(0.38066, 0.47583, 0.2855))

    def test_shading_inside(self):
        w = World.default()
        w.light = Light(Point(0, 0.25, 0), Color(1, 1, 1))
        c = w.shade_hit(Intersection(0.5, w.objects[1]).prepare_computations(Ray(Point(0, 0, 0), Vector(0, 0, 1))))
        self.assertEqual(c, Color(0.90498, 0.90498, 0.90498))

    def test_color_when_ray_miss(self):
        w = World.default()
        self.assertEqual(w.color_at(Ray(Point(0, 0, -5), Vector(0, 1, 0))), Color(0, 0, 0))

    def test_color_when_ray_hit(self):
        w = World.default()
        self.assertEqual(w.color_at(Ray(Point(0, 0, -5), Vector(0, 0, 1))), Color(0.38066, 0.47583, 0.2855))

    def test_color_when_behind_ray(self):
        w = World.default()
        w.objects[0].material.ambient = 1
        w.objects[1].material.ambient = 1
        self.assertEqual(w.color_at(Ray(Point(0, 0, 0.75), Vector(0, 0, -1))), w.objects[1].material.color)
