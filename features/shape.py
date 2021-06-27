from features.intersection import Intersections, Intersection
from features.material import Material
from features.matrix import Matrix
from features.tuple import Point, Vector


class Shape:
    def __init__(self, transform=None, material=None):
        self.transform = Matrix.identity(4) if not transform else transform
        self.material = Material() if not material else material

    def set_transform(self, t):
        self.transform = t

    def normal_at(self, point):
        obj_norm = self.local_normal_at(self.transform.inverse() * point)
        world_norm = self.transform.inverse().transpose() * obj_norm
        world_norm.w = 0
        return world_norm.normalize()

    def local_normal_at(self, point):
        pass

    def intersect(self, ray):
        return self.local_intersect(ray.transform(self.transform.inverse()))

    def local_intersect(self, ray):
        pass


class Test(Shape):
    def __init__(self, transform=None, material=None):
        super().__init__(transform, material)
        self.saved_ray = None

    def local_intersect(self, ray):
        self.saved_ray = ray

    def local_normal_at(self, point: Point):
        return Vector(point.x, point.y, point.z)


class Sphere(Shape):
    def __init__(self, origin=None, transform=None, material=None):
        self.origin = Point(0, 0, 0) if not origin else origin
        super().__init__(transform, material)

    def __eq__(self, other):
        return isinstance(other, Sphere) and self.origin == other.origin and self.transform == other.transform and \
               self.material == other.material

    def local_normal_at(self, point):
        return point - self.origin

    def local_intersect(self, ray):
        sphere_to_ray = ray.origin - self.origin

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        d = b ** 2 - 4 * a * c

        if d < 0:
            return Intersections()

        t1 = (-b - d ** 0.5) / (2 * a)
        t2 = (-b + d ** 0.5) / (2 * a)
        return Intersections(Intersection(t1, self), Intersection(t2, self))


class Plane(Shape):
    def __init__(self, transform=None, material=None):
        super().__init__(transform, material)

    def local_normal_at(self, point):
        return Vector(0, 1, 0)

    def local_intersect(self, ray):
        if abs(ray.direction.y) < 0.00001:
            return Intersections()
        return Intersections(Intersection(-ray.origin.y / ray.direction.y, self))
