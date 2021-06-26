import unittest

import numpy as np

from features.matrix import Translation, Scaling, Rotation, Shearing
from features.tuple import Point, Vector


class TestTransformations(unittest.TestCase):
    def test_point_translation(self):
        self.assertEqual(Translation(5, -3, 2) * Point(-3, 4, 5), Point(2, 1, 7))

    def test_inverse_translation(self):
        self.assertEqual(Translation(5, -3, 2).inverse() * Point(-3, 4, 5), Point(-8, 7, 3))

    def test_vector_translation(self):
        self.assertEqual(Translation(5, 3, 2) * Vector(-3, 4, 5), Vector(-3, 4, 5))

    def test_point_scaling(self):
        self.assertEqual(Scaling(2, 3, 4) * Point(-4, 6, 8), Point(-8, 18, 32))

    def test_vector_scaling(self):
        self.assertEqual(Scaling(2, 3, 4) * Vector(-4, 6, 8), Vector(-8, 18, 32))

    def test_inverse_scaling(self):
        self.assertEqual(Scaling(2, 3, 4).inverse() * Vector(-4, 6, 8), Vector(-2, 2, 2))

    def test_x_rotation(self):
        self.assertEqual(Rotation(np.pi / 4, 0, 0) * Point(0, 1, 0), Point(0, 2 ** 0.5 / 2, 2 ** 0.5 / 2))
        self.assertEqual(Rotation(np.pi / 2, 0, 0) * Point(0, 1, 0), Point(0, 0, 1))

    def test_inverse_x_rotation(self):
        self.assertEqual(Rotation(np.pi / 4, 0, 0).inverse() * Point(0, 1, 0), Point(0, 2 ** 0.5 / 2, -(2 ** 0.5) / 2))

    def test_y_rotation(self):
        self.assertEqual(Rotation(0, np.pi / 4, 0) * Point(0, 0, 1), Point(2 ** 0.5 / 2, 0, 2 ** 0.5 / 2))
        self.assertEqual(Rotation(0, np.pi / 2, 0) * Point(0, 0, 1), Point(1, 0, 0))

    def test_z_rotation(self):
        self.assertEqual(Rotation(0, 0, np.pi / 4) * Point(0, 1, 0), Point(-(2 ** 0.5) / 2, 2 ** 0.5 / 2, 0))
        self.assertEqual(Rotation(0, 0, np.pi / 2) * Point(0, 1, 0), Point(-1, 0, 0))

    def test_shearing_x_to_y(self):
        self.assertEqual(Shearing(1, 0, 0, 0, 0, 0) * Point(2, 3, 4), Point(5, 3, 4))

    def test_shearing_x_to_z(self):
        self.assertEqual(Shearing(0, 1, 0, 0, 0, 0) * Point(2, 3, 4), Point(6, 3, 4))

    def test_shearing_y_to_x(self):
        self.assertEqual(Shearing(0, 0, 1, 0, 0, 0) * Point(2, 3, 4), Point(2, 5, 4))

    def test_shearing_y_to_z(self):
        self.assertEqual(Shearing(0, 0, 0, 1, 0, 0) * Point(2, 3, 4), Point(2, 7, 4))

    def test_shearing_z_to_x(self):
        self.assertEqual(Shearing(0, 0, 0, 0, 1, 0) * Point(2, 3, 4), Point(2, 3, 6))

    def test_shearing_z_to_y(self):
        self.assertEqual(Shearing(0, 0, 0, 0, 0, 1) * Point(2, 3, 4), Point(2, 3, 7))

    def test_sequential(self):
        p = Point(1, 0, 1)
        A = Rotation(np.pi / 2, 0, 0)
        B = Scaling(5, 5, 5)
        C = Translation(10, 5, 7)

        self.assertEqual(A * p, Point(1, -1, 0))
        self.assertEqual(B * A * p, Point(5, -5, 0))
        self.assertEqual(C * B * A * p, Point(15, 0, 7))
