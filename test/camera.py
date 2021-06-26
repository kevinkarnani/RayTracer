import unittest
import numpy as np

from features.camera import Camera
from features.matrix import Matrix, Rotation, Translation, view_transform
from features.tuple import Point, Vector, Color
from features.world import World


class TestCamera(unittest.TestCase):
    def test_creation(self):
        c = Camera(160, 120, np.pi / 2)
        self.assertEqual(c.h_size, 160)
        self.assertEqual(c.v_size, 120)
        self.assertEqual(c.fov, np.pi / 2)
        self.assertEqual(c.transform, Matrix.identity(4))

    def test_horizontal_pixel(self):
        self.assertAlmostEqual(Camera(200, 125, np.pi / 2).pixel_size, 0.01)

    def test_vertical_pixel(self):
        self.assertAlmostEqual(Camera(125, 200, np.pi / 2).pixel_size, 0.01)

    def test_ray_canvas_center(self):
        r = Camera(201, 101, np.pi / 2).ray_for_pixel(100, 50)
        self.assertEqual(r.origin, Point(0, 0, 0))
        self.assertEqual(r.direction, Vector(0, 0, -1))

    def test_ray_canvas_corner(self):
        r = Camera(201, 101, np.pi / 2).ray_for_pixel(0, 0)
        self.assertEqual(r.origin, Point(0, 0, 0))
        self.assertEqual(r.direction, Vector(0.66519, 0.33259, -0.66851))

    def test_ray_transformed(self):
        r = Camera(201, 101, np.pi / 2, Rotation(0, np.pi / 4, 0) * Translation(0, -2, 5)).ray_for_pixel(100, 50)
        self.assertEqual(r.origin, Point(0, 2, -5))
        self.assertEqual(r.direction, Vector(np.sqrt(2) / 2, 0, -np.sqrt(2) / 2))

    def test_render_world(self):
        w = World.default()
        c = Camera(11, 11, np.pi / 2)
        c.transform = view_transform(Point(0, 0, -5), Point(0, 0, 0), Vector(0, 1, 0))
        image = c.render(w)
        self.assertEqual(image.pixel_at(5, 5), Color(0.38066, 0.47583, 0.2855))
