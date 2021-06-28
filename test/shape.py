import unittest

import numpy as np

from features.material import Material
from features.matrix import Translation, Scaling, Matrix, Rotation
from features.ray import Ray
from features.shape import Sphere, Test, Plane, Cube, Cylinder, Cone
from features.tuple import Point, Vector


class TestShape(unittest.TestCase):
    def test_ray_intersects_twice(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 4)
        self.assertEqual(xs[1].t, 6)

    def test_ray_intersects_once(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 5)
        self.assertEqual(xs[1].t, 5)

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
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, -1)
        self.assertEqual(xs[1].t, 1)

    def test_sphere_behind_ray(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, -6)
        self.assertEqual(xs[1].t, -4)

    def test_intersect_sets_object(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].obj, s)
        self.assertEqual(xs[1].obj, s)

    def test_shape_default_transformation(self):
        s = Test()
        self.assertEqual(s.transform, Matrix.identity(4))

    def test_changing_shape_transformation(self):
        s = Test()
        s.set_transform(Translation(2, 3, 4))
        self.assertEqual(s.transform, Translation(2, 3, 4))

    def test_intersecting_scaled_shape(self):
        s = Test()
        s.set_transform(Scaling(2, 2, 2))
        s.intersect(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(s.saved_ray.origin, Point(0, 0, -2.5))
        self.assertEqual(s.saved_ray.direction, Vector(0, 0, 0.5))

    def test_intersecting_translated_shape(self):
        s = Test()
        s.set_transform(Translation(5, 0, 0))
        s.intersect(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(s.saved_ray.origin, Point(-5, 0, -5))
        self.assertEqual(s.saved_ray.direction, Vector(0, 0, 1))

    def test_normal_x(self):
        self.assertEqual(Sphere().normal_at(Point(1, 0, 0)), Vector(1, 0, 0))

    def test_normal_y(self):
        self.assertEqual(Sphere().normal_at(Point(0, 1, 0)), Vector(0, 1, 0))

    def test_normal_z(self):
        self.assertEqual(Sphere().normal_at(Point(0, 0, 1)), Vector(0, 0, 1))

    def test_non_axial_normal(self):
        a = 3 ** 0.5 / 3
        self.assertEqual(Sphere().normal_at(Point(a, a, a)), Vector(a, a, a))

    def test_normal_is_normalized(self):
        s = Sphere()
        a = 3 ** 0.5 / 3
        n = s.normal_at(Point(a, a, a))
        self.assertEqual(n, n.normalize())

    def test_translated_normal(self):
        s = Test()
        s.set_transform(Translation(0, 1, 0))
        self.assertEqual(s.normal_at(Point(0, 1.70711, -0.70711)), Vector(0, 0.70711, -0.70711))

    def test_transformed_normal(self):
        s = Test()
        s.set_transform(Scaling(1, 0.5, 1) * Rotation(0, 0, np.pi / 5))
        self.assertEqual(s.normal_at(Point(0, 2 ** -0.5, -(2 ** -0.5))), Vector(0, 0.97014, -0.24254))

    def test_default_material(self):
        s = Test()
        self.assertEqual(s.material, Material())

    def test_assign_material(self):
        s = Test(material=Material(ambient=1))
        self.assertEqual(s.material, Material(ambient=1))
        self.assertEqual(s.material.ambient, 1)

    def test_plane_constant_normal(self):
        p = Plane()
        self.assertEqual(p.local_normal_at(Point(0, 0, 0)), Vector(0, 1, 0))
        self.assertEqual(p.local_normal_at(Point(10, 0, -10)), Vector(0, 1, 0))
        self.assertEqual(p.local_normal_at(Point(-5, 0, 150)), Vector(0, 1, 0))

    def test_ray_parallel_to_plane(self):
        p = Plane()
        self.assertEqual(p.local_intersect(Ray(Point(0, 10, 0), Vector(0, 0, 1))).count, 0)

    def test_coplanar_ray(self):
        p = Plane()
        self.assertEqual(p.local_intersect(Ray(Point(0, 0, 0), Vector(0, 0, 1))).count, 0)

    def test_ray_above_intersect(self):
        p = Plane()
        xs = p.local_intersect(Ray(Point(0, 1, 0), Vector(0, -1, 0)))
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[0].obj, p)

    def test_ray_below_intersect(self):
        p = Plane()
        xs = p.local_intersect(Ray(Point(0, -1, 0), Vector(0, 1, 0)))
        self.assertEqual(xs[0].t, 1)
        self.assertEqual(xs[0].obj, p)

    def test_glassy_sphere(self):
        s = Sphere.glassy()
        self.assertEqual(s.material.transparency, 1)
        self.assertEqual(s.material.refractive_index, 1.5)

    def test_ray_intersects_cube(self):
        c = Cube()
        xs = c.local_intersect(Ray(Point(5, 0.5, 0), Vector(-1, 0, 0)))
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 4)
        self.assertEqual(xs[1].t, 6)
        xs = c.local_intersect(Ray(Point(0, 0.5, 0), Vector(0, 0, 1)))
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, -1)
        self.assertEqual(xs[1].t, 1)

    def test_ray_misses_cube(self):
        c = Cube()
        xs = c.local_intersect(Ray(Point(2, 0, 2), Vector(0, 0, -1)))
        self.assertEqual(xs.count, 0)
        xs = c.local_intersect(Ray(Point(0, 2, 2), Vector(0, -1, 0)))
        self.assertEqual(xs.count, 0)
        xs = c.local_intersect(Ray(Point(2, 2, 0), Vector(-1, 0, 0)))
        self.assertEqual(xs.count, 0)

    def test_normal_cube(self):
        c = Cube()
        self.assertEqual(c.normal_at(Point(1, 0.5, -0.8)), Vector(1, 0, 0))
        self.assertEqual(c.normal_at(Point(-1, -0.2, 0.9)), Vector(-1, 0, 0))
        self.assertEqual(c.normal_at(Point(-0.4, 1, -0.1)), Vector(0, 1, 0))
        self.assertEqual(c.normal_at(Point(0.3, -1, -0.7)), Vector(0, -1, 0))
        self.assertEqual(c.normal_at(Point(-0.6, 0.3, 1)), Vector(0, 0, 1))
        self.assertEqual(c.normal_at(Point(0.4, 0.4, -1)), Vector(0, 0, -1))
        self.assertEqual(c.normal_at(Point(1, 1, 1)), Vector(1, 0, 0))
        self.assertEqual(c.normal_at(Point(-1, -1, -1)), Vector(-1, 0, 0))

    def test_ray_misses_cylinder(self):
        cy = Cylinder()
        self.assertEqual(cy.local_intersect(Ray(Point(1, 0, 0), Vector(0, 1, 0))).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 0, 0), Vector(0, 1, 0))).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 0, -5), Vector(1, 1, 1))).count, 0)

    def test_ray_strikes_cylinder(self):
        cy = Cylinder()
        xs = cy.local_intersect(Ray(Point(1, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 5)
        self.assertEqual(xs[1].t, 5)
        xs = cy.local_intersect(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 4)
        self.assertEqual(xs[1].t, 6)
        xs = cy.local_intersect(Ray(Point(0.5, 0, -5), Vector(0.1, 1, 1).normalize()))
        self.assertEqual(xs.count, 2)
        self.assertAlmostEqual(xs[0].t, 6.80798, places=5)
        self.assertAlmostEqual(xs[1].t, 7.08872, places=5)

    def test_normal_cylinder(self):
        cy = Cylinder()
        self.assertEqual(cy.local_normal_at(Point(1, 0, 0)), Vector(1, 0, 0))
        self.assertEqual(cy.local_normal_at(Point(0, 5, -1)), Vector(0, 0, -1))
        self.assertEqual(cy.local_normal_at(Point(0, -2, 1)), Vector(0, 0, 1))
        self.assertEqual(cy.local_normal_at(Point(-1, 1, 0)), Vector(-1, 0, 0))

    def test_infinite_cylinder_limits(self):
        cy = Cylinder()
        self.assertEqual(cy.minimum, -float('inf'))
        self.assertEqual(cy.maximum, float('inf'))

    def test_finite_cylinder_limits(self):
        cy = Cylinder(minimum=1, maximum=2)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 1.5, 0), Vector(0.1, 1, 0).normalize())).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 3, -5), Vector(0, 0, 1))).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 0, -5), Vector(0, 0, 1))).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 2, -5), Vector(0, 0, 1))).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 1, -5), Vector(0, 0, 1))).count, 0)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 1.5, -2), Vector(0, 0, 1))).count, 2)

    def test_default_cylinder(self):
        self.assertFalse(Cylinder().closed)

    def test_intersecting_cylinder_caps(self):
        cy = Cylinder(minimum=1, maximum=2, closed=True)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 3, 0), Vector(0, -1, 0))).count, 2)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 3, -2), Vector(0, -1, 2).normalize())).count, 2)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 4, -2), Vector(0, -1, 1))).count, 2)
        self.assertEqual(cy.local_intersect(Ray(Point(0, 0, -2), Vector(0, 1, 2))).count, 2)
        self.assertEqual(cy.local_intersect(Ray(Point(0, -1, -2), Vector(0, 1, 1))).count, 2)

    def test_normal_at_caps(self):
        cy = Cylinder(minimum=1, maximum=2, closed=True)
        self.assertEqual(cy.normal_at(Point(0, 1, 0)), Vector(0, -1, 0))
        self.assertEqual(cy.normal_at(Point(0.5, 1, 0)), Vector(0, -1, 0))
        self.assertEqual(cy.normal_at(Point(0, 1, 0.5)), Vector(0, -1, 0))
        self.assertEqual(cy.normal_at(Point(0, 2, 0)), Vector(0, 1, 0))
        self.assertEqual(cy.normal_at(Point(0.5, 2, 0)), Vector(0, 1, 0))
        self.assertEqual(cy.normal_at(Point(0, 2, 0.5)), Vector(0, 1, 0))

    def test_ray_intersects_cone(self):
        co = Cone()
        xs = co.local_intersect(Ray(Point(0, 0, -5), Vector(0, 0, 1)))
        self.assertEqual(xs.count, 2)
        self.assertEqual(xs[0].t, 5)
        self.assertEqual(xs[1].t, 5)
        xs = co.local_intersect(Ray(Point(0, 0, -5), Vector(1, 1, 1).normalize()))
        self.assertEqual(xs.count, 2)
        self.assertAlmostEqual(xs[0].t, 8.66205, places=2)
        self.assertAlmostEqual(xs[1].t, 8.66205, places=2)
        xs = co.local_intersect(Ray(Point(1, 1, -5), Vector(-0.5, -1, 1).normalize()))
        self.assertEqual(xs.count, 2)
        self.assertAlmostEqual(xs[0].t, 4.55006, places=5)
        self.assertAlmostEqual(xs[1].t, 49.44994, places=5)

    def test_parallel_ray_intersects_cone(self):
        co = Cone()
        xs = co.local_intersect(Ray(Point(0, 0, -1), Vector(0, 1, 1).normalize()))
        self.assertEqual(xs.count, 1)
        self.assertAlmostEqual(xs[0].t, 0.35355, places=5)

    def test_cone_caps(self):
        co = Cone(minimum=-0.5, maximum=0.5, closed=True)
        self.assertEqual(co.local_intersect(Ray(Point(0, 0, -5), Vector(0, 1, 0))).count, 0)
        self.assertEqual(co.local_intersect(Ray(Point(0, 0, -0.25), Vector(0, 1, 1))).count, 2)
        self.assertEqual(co.local_intersect(Ray(Point(0, 0, -0.25), Vector(0, 1, 0))).count, 4)

    def test_cone_normal(self):
        co = Cone()
        self.assertEqual(co.local_normal_at(Point(0, 0, 0)), Vector(0, 0, 0))
        self.assertEqual(co.local_normal_at(Point(1, 1, 1)), Vector(1, -(2 ** 0.5), 1))
        self.assertEqual(co.local_normal_at(Point(-1, -1, 0)), Vector(-1, 1, 0))

    def test_parent(self):
        s = Test()
        self.assertIsNone(s.parent)
