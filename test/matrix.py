import unittest

from features.matrix import Matrix
from features.tuple import Tuple


class TestMatrix(unittest.TestCase):
    def test_matrix(self):
        m = Matrix(
            [
                [1, 2, 3, 4],
                [5.5, 6.5, 7.5, 8.5],
                [9, 10, 11, 12],
                [13.5, 14.5, 15.5, 16.5],
            ]
        )
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[0][3], 4)
        self.assertEqual(m[1][0], 5.5)
        self.assertEqual(m[3][2], 15.5)

    def test_size(self):
        m2 = Matrix([[-3, -5], [1, -2]])
        self.assertEqual(m2.size, 2)

        m3 = Matrix([[-3, 5, 0], [1, 2, 0], [0, 1, 1]])
        self.assertEqual(m3.size, 3)

    def test_matrix_multiplication(self):
        m1 = Matrix([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]])

        m2 = Matrix([[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]])
        expected = Matrix(
            [
                [24, 49, 98, 196],
                [31, 64, 128, 256],
                [38, 79, 158, 316],
                [45, 94, 188, 376],
            ]
        )
        self.assertEqual(m1 * m2, expected)

    def test_tuple_multiplication(self):
        m1 = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
        t1 = Tuple(1, 2, 3, 1)
        expected = Tuple(18, 24, 33, 1)
        self.assertEqual(m1 * t1, expected)

    def test_identity(self):
        m1 = Matrix([[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]])
        self.assertEqual(m1 * Matrix.identity(4), m1)
        t1 = Tuple(1, 2, 3, 4)
        self.assertEqual(Matrix.identity(4) * t1, t1)

    def test_transpose(self):
        m1 = Matrix([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
        expected = Matrix([[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
        self.assertEqual(m1.transpose(), expected)
        identity = Matrix.identity(4)
        self.assertEqual(identity.transpose(), identity)

    def test_determinant(self):
        m1 = Matrix([[1, 5], [-3, 2]])
        self.assertEqual(m1.determinant(), 17)

        m2 = Matrix([[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
        self.assertEqual(m2.determinant(), -196)

        m3 = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
        self.assertEqual(m3.determinant(), -4071)

    def test_invertible(self):
        m1 = Matrix([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
        self.assertEqual(m1.determinant(), -2120)
        self.assertTrue(m1.invertible())

        m2 = Matrix([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
        self.assertEqual(m2.determinant(), 0)
        self.assertFalse(m2.invertible())

    def test_inverse(self):
        a = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
        b = a.inverse()
        self.assertEqual(a.determinant(), 532)
        expected = Matrix(
            [
                [0.21805, 0.45113, 0.24060, -0.04511],
                [-0.80827, -1.45677, -0.44361, 0.52068],
                [-0.07895, -0.22368, -0.05263, 0.19737],
                [-0.52256, -0.81391, -0.30075, 0.30639],
            ]
        )
        self.assertEqual(b, expected)

        c = Matrix([[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
        c_inverse = Matrix(
            [
                [-0.15385, -0.15385, -0.28205, -0.53846],
                [-0.07692, 0.12308, 0.02564, 0.03077],
                [0.35897, 0.35897, 0.43590, 0.92308],
                [-0.69231, -0.69231, -0.76923, -1.92308],
            ]
        )
        self.assertEqual(c.inverse(), c_inverse)

        d = Matrix([[9, 3, 0, 9], [-5, -2, -6, -3], [-4, 9, 6, 4], [-7, 6, 6, 2]])
        d_inverse = Matrix(
            [
                [-0.04074, -0.07778, 0.14444, -0.22222],
                [-0.07778, 0.03333, 0.36667, -0.33333],
                [-0.02901, -0.14630, -0.10926, 0.12963],
                [0.17778, 0.06667, -0.26667, 0.33333],
            ]
        )
        self.assertEqual(d.inverse(), d_inverse)

    def test_multiply_by_inverse(self):
        a = Matrix([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
        b = Matrix([[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, 5]])
        c = a * b
        self.assertEqual(c * b.inverse(), a)