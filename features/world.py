import numpy as np

from features.intersection import Intersections
from features.light import Light
from features.material import Material
from features.matrix import Scaling
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Color, Point


class World:
    def __init__(self):
        self.light = None
        self.objects = []

    @staticmethod
    def default():
        w = World()
        s1, s2 = Sphere(), Sphere()
        s1.material = Material(color=Color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2)
        s2.material = Material()
        s2.set_transform(Scaling(0.5, 0.5, 0.5))
        w.light = Light(Point(-10, 10, -10), Color(1, 1, 1))
        w.objects = [s1, s2]
        return w

    def intersect(self, r):
        xs = Intersections()
        for obj in self.objects:
            xs.extend(obj.intersect(r))
        xs.sort()
        return xs

    def shade_hit(self, comps, remaining=5):
        shadowed = self.is_shadowed(comps.over_point)

        surface = comps.obj.material.lighting(comps.obj, self.light, comps.over_point, comps.eye_v, comps.normal_v,
                                              shadowed)
        reflected = self.reflected_color(comps, remaining)
        refracted = self.refracted_color(comps, remaining)

        m = comps.obj.material
        if m.transparency > 0 and m.reflective > 0:
            reflectance = comps.schlick()
            return surface + reflected * reflectance + refracted * (1 - reflectance)
        else:
            return surface + reflected + refracted

    def color_at(self, r, remaining=5):
        hit = self.intersect(r).hit()
        return Color(0, 0, 0) if not hit else self.shade_hit(hit.prepare_computations(r), remaining)

    def is_shadowed(self, point):
        v = self.light.position - point
        hit = self.intersect(Ray(point, v.normalize())).hit()
        return hit and hit.t < v.magnitude()

    def reflected_color(self, comps, remaining=5):
        if not comps.obj.material.reflective or remaining <= 0:
            return Color(0, 0, 0)

        return self.color_at(Ray(comps.over_point, comps.reflect_v), remaining - 1) * comps.obj.material.reflective

    def refracted_color(self, comps, remaining=5):
        if not comps.obj.material.transparency or remaining <= 0:
            return Color(0, 0, 0)

        n_ratio = comps.n1 / comps.n2
        cos_i = comps.eye_v.dot(comps.normal_v)
        sin2_t = n_ratio ** 2 * (1 - cos_i ** 2)
        if sin2_t > 1:
            return Color(0, 0, 0)

        cos_t = np.sqrt(1 - sin2_t)
        direction = comps.normal_v * (n_ratio * cos_i - cos_t) - comps.eye_v * n_ratio

        return self.color_at(Ray(comps.under_point, direction), remaining - 1) * comps.obj.material.transparency
