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

    def shade_hit(self, comps):
        return comps.obj.material.lighting(self.light, comps.point, comps.eye_v, comps.normal_v,
                                           self.is_shadowed(comps.over_point))

    def color_at(self, r):
        hit = self.intersect(r).hit()
        return Color(0, 0, 0) if hit is None else self.shade_hit(hit.prepare_computations(r))

    def is_shadowed(self, point):
        v = self.light.position - point
        hit = self.intersect(Ray(point, v.normalize())).hit()
        return hit and hit.t < v.magnitude()
