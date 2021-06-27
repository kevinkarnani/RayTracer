import unittest

from features.intersection import Intersection, Intersections
from features.light import Light
from features.material import Material
from features.matrix import Scaling, Translation
from features.pattern import Test
from features.ray import Ray
from features.shape import Sphere, Plane
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

    def test_collinear_no_shadow(self):
        w = World.default()
        self.assertFalse(w.is_shadowed(Point(0, 10, 0)))

    def test_object_shadow(self):
        w = World.default()
        self.assertTrue(w.is_shadowed(Point(10, -10, 10)))

    def test_behind_light_no_shadow(self):
        w = World.default()
        self.assertFalse(w.is_shadowed(Point(-20, 20, -20)))

    def test_between_object_no_light(self):
        w = World.default()
        self.assertFalse(w.is_shadowed(Point(-2, 2, -2)))

    def test_given_shadow_intersection(self):
        w = World()
        w.light = Light(Point(0, 0, -10), Color(1, 1, 1))
        w.objects.append(Sphere())
        s = Sphere()
        s.set_transform(Translation(0, 0, 10))
        w.objects.append(s)
        self.assertEqual(w.shade_hit(Intersection(4, s).prepare_computations(Ray(Point(0, 0, 5), Vector(0, 0, 1)))),
                         Color(0.1, 0.1, 0.1))

    def test_reflect_when_not_reflective(self):
        w = World.default()
        w.objects[1].material.ambient = 1
        comps = Intersection(1, w.objects[1]).prepare_computations(Ray(Point(0, 0, 0), Vector(0, 0, 1)))
        self.assertEqual(w.reflected_color(comps), Color(0, 0, 0))

    def test_reflect_off_reflective(self):
        w = World.default()
        p = Plane()
        p.material.reflective = 0.5
        p.transform = Translation(0, -1, 0)
        w.objects.append(p)
        comps = Intersection(2 ** 0.5, p).prepare_computations(
            Ray(Point(0, 0, -3), Vector(0, -(2 ** -0.5), (2 ** -0.5))))
        self.assertEqual(w.reflected_color(comps), Color(0.19032, 0.2379, 0.14274))

    def test_shade_reflective(self):
        w = World.default()
        p = Plane()
        p.material.reflective = 0.5
        p.transform = Translation(0, -1, 0)
        w.objects.append(p)
        comps = Intersection(2 ** 0.5, p).prepare_computations(
            Ray(Point(0, 0, -3), Vector(0, -(2 ** -0.5), (2 ** -0.5))))
        self.assertEqual(w.shade_hit(comps), Color(0.87677, 0.92436, 0.82918))

    def test_color_mutually_reflective(self):
        w = World()
        w.light = Light(Point(0, 0, 0), Color(1, 1, 1))
        lower = Plane()
        lower.material.reflective = 1
        lower.transform = Translation(0, -1, 0)
        w.objects.append(lower)
        upper = Plane()
        upper.material.reflective = 1
        upper.transform = Translation(0, 1, 0)
        w.objects.append(upper)
        self.assertIsNotNone(w.color_at(Ray(Point(0, 0, 0), Vector(0, 1, 0))))

    def test_reflect_max_depth(self):
        w = World.default()
        shape = Plane()
        shape.material.reflective = 0.5
        shape.transform = Translation(0, -1, 0)
        w.objects.append(shape)
        comps = Intersection(2 ** 0.5, shape).prepare_computations(
            Ray(Point(0, 0, -3), Vector(0, -(2 ** -0.5), (2 ** -0.5))))
        self.assertEqual(w.reflected_color(comps, 0), Color(0, 0, 0))

    def test_refract_opaque(self):
        w = World.default()
        shape = w.objects[0]
        xs = Intersections(Intersection(4, shape), Intersection(6, shape))
        comps = xs[0].prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1)), xs)
        self.assertEqual(w.refracted_color(comps), Color(0, 0, 0))

    def test_refract_max_depth(self):
        w = World.default()
        shape = w.objects[0]
        shape.material.transparency = 1
        shape.material.refractive_index = 1.5
        xs = Intersections(Intersection(4, shape), Intersection(6, shape))
        comps = xs[0].prepare_computations(Ray(Point(0, 0, -5), Vector(0, 0, 1)), xs)
        self.assertEqual(w.refracted_color(comps, 0), Color(0, 0, 0))

    def test_refract_after_reflect(self):
        w = World.default()
        shape = w.objects[0]
        shape.material.transparency = 1
        shape.material.refractive_index = 1.5
        xs = Intersections(Intersection(-(2 ** -0.5), shape), Intersection((2 ** -0.5), shape))
        comps = xs[1].prepare_computations(Ray(Point(0, 0, (2 ** -0.5)), Vector(0, 1, 0)), xs)
        self.assertEqual(w.refracted_color(comps), Color(0, 0, 0))

    def test_color_after_refract(self):
        w = World.default()
        s1, s2 = w.objects
        s1.material.ambient = 1
        s1.material.pattern = Test(Color(1, 1, 1), Color(0, 0, 0))
        s2.material.transparency = 1
        s2.material.refractive_index = 1.5
        xs = Intersections(Intersection(-0.9899, s1), Intersection(-0.4899, s2), Intersection(0.4899, s2),
                           Intersection(0.9899, s1))
        comps = xs[2].prepare_computations(Ray(Point(0, 0, 0.1), Vector(0, 1, 0)), xs)
        self.assertEqual(w.refracted_color(comps), Color(0, 0.99888, 0.04725))

    def test_shade_transparent_material(self):
        w = World.default()
        floor = Plane()
        floor.set_transform(Translation(0, -1, 0))
        floor.material.transparency = 0.5
        floor.material.refractive_index = 1.5
        w.objects.append(floor)

        ball = Sphere()
        ball.material.color = Color(1, 0, 0)
        ball.material.ambient = 0.5
        ball.set_transform(Translation(0, -3.5, -0.5))
        w.objects.append(ball)

        xs = Intersections(Intersection(2 ** 0.5, floor))
        comps = xs[0].prepare_computations(Ray(Point(0, 0, -3), Vector(0, -(2 ** -0.5), (2 ** -0.5))), xs)
        self.assertEqual(w.shade_hit(comps), Color(0.93642, 0.68642, 0.68642))

    def test_shade_reflective_transparent(self):
        w = World.default()
        floor = Plane()
        floor.set_transform(Translation(0, -1, 0))
        floor.material.reflective = 0.5
        floor.material.transparency = 0.5
        floor.material.refractive_index = 1.5
        w.objects.append(floor)

        ball = Sphere()
        ball.material.color = Color(1, 0, 0)
        ball.material.ambient = 0.5
        ball.set_transform(Translation(0, -3.5, -0.5))
        w.objects.append(ball)

        xs = Intersections(Intersection(2 ** 0.5, floor))
        comps = xs[0].prepare_computations(Ray(Point(0, 0, -3), Vector(0, -(2 ** -0.5), (2 ** -0.5))), xs)
        self.assertEqual(w.shade_hit(comps), Color(0.93391, 0.69643, 0.69243))
