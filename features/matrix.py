import numpy as np

from features.tuple import Tuple


class Matrix:
    def __init__(self, matrix):
        self.size = len(matrix)
        if len(matrix[0]) != self.size:
            raise Exception
        self.matrix = np.array(matrix)

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __eq__(self, other):
        return np.allclose(self.matrix, other.matrix, rtol=10 ** -4) if isinstance(other, Matrix) else False

    def __matmul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.matrix @ other.matrix)
        else:
            print("Invalid Matrix")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.__matmul__(other)
        elif isinstance(other, int) or isinstance(other, float):
            return Matrix(self.matrix * other)
        elif isinstance(other, Tuple):
            return Tuple(
                Tuple(*(self[0])).dot(other),
                Tuple(*(self[1])).dot(other),
                Tuple(*(self[2])).dot(other),
                Tuple(*(self[3])).dot(other),
            )
        else:
            print("Cannot multiply Matrix by anything apart from Matrix, Integer, Float, or Tuple")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        output = ""
        for line in self.matrix:
            output += " ".join(str(x) for x in line) + "\n"
        return output

    @staticmethod
    def identity(size):
        return Matrix(np.eye(size))

    def transpose(self):
        return Matrix(self.matrix.T)

    def determinant(self):
        return np.round(np.linalg.det(self.matrix), 5)

    def invertible(self):
        return self.determinant() != 0

    def inverse(self):
        if self.invertible():
            return Matrix(np.linalg.inv(self.matrix))
        else:
            raise Exception


class Translation(Matrix):
    def __init__(self, x, y, z):
        super().__init__(np.eye(4))
        self.matrix[:3, 3] = [x, y, z]


class Scaling(Matrix):
    def __init__(self, x, y, z):
        super().__init__(np.diag([x, y, z, 1]))


class Rotation(Matrix):
    def __init__(self, x_theta=None, y_theta=None, z_theta=None):
        matrix = np.eye(4)

        if x_theta:
            matrix_x = np.eye(4)
            matrix_x[1:3, 1:3] = [[np.cos(x_theta), -np.sin(x_theta)], [np.sin(x_theta), np.cos(x_theta)]]
            matrix = matrix_x @ matrix

        if y_theta:
            matrix_y = np.eye(4)
            matrix_y[::2, ::2] = [[np.cos(y_theta), np.sin(y_theta)], [-np.sin(y_theta), np.cos(y_theta)]]
            matrix = matrix_y @ matrix

        if z_theta:
            matrix_z = np.eye(4)
            matrix_z[:2, :2] = [[np.cos(z_theta), -np.sin(z_theta)], [np.sin(z_theta), np.cos(z_theta)]]
            matrix = matrix_z @ matrix

        super().__init__(matrix)


class Shearing(Matrix):
    def __init__(self, x_y, x_z, y_x, y_z, z_x, z_y):
        matrix = np.eye(4)
        matrix[:3, :3] = [[1, x_y, x_z], [y_x, 1, y_z], [z_x, z_y, 1]]
        super().__init__(matrix)