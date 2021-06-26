import numpy as np

from features.intersection import Intersection
from features.matrix import Matrix
from features.tuple import Point


class Sphere:
    def __init__(self, origin=Point(0, 0, 0), transform=Matrix.identity(4)):
        self.origin = origin
        self.transform = transform

    def intersect(self, ray):
        ray = ray.transform(self.transform.inverse())
        sphere_to_ray = ray.origin - self.origin

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        d = b ** 2 - 4 * a * c

        if d < 0:
            return Intersection(np.array([]), self)

        t1 = (-b - d ** 0.5) / (2 * a)
        t2 = (-b + d ** 0.5) / (2 * a)
        return Intersection(np.vstack([t1, t2]), self)

    def set_transform(self, t):
        self.transform = t
