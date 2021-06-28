from features.bounds import Bounds
from features.intersection import Intersections, Intersection
from features.material import Material
from features.matrix import Matrix
from features.tuple import Point, Vector


class Shape:
    def __init__(self, transform=None, material=None, parent=None):
        self.transform = Matrix.identity(4) if not transform else transform
        self.material = Material() if not material else material
        self.parent = parent
        self.box = None

    def set_transform(self, t):
        self.transform = t

    def normal_at(self, point):
        local_point = self.world_to_object(point)
        local_normal = self.local_normal_at(local_point)
        return self.normal_to_world(local_normal)

    def local_normal_at(self, point):
        pass

    def intersect(self, ray):
        return self.local_intersect(ray.transform(self.transform.inverse()))

    def local_intersect(self, ray):
        pass

    def world_to_object(self, point):
        if self.parent:
            point = self.parent.world_to_object(point)

        return self.transform.inverse() * point

    def bounds(self):
        pass

    def normal_to_world(self, normal):
        normal = self.transform.inverse().transpose() * normal
        normal.w = 0
        normal = normal.normalize()

        if self.parent:
            normal = self.parent.normal_to_world(normal)

        return normal


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

    @staticmethod
    def glassy():
        s = Sphere()
        s.material.transparency = 1
        s.material.refractive_index = 1.5
        return s

    def bounds(self):
        self.box = Bounds(minimum=Point(-1, -1, -1), maximum=Point(1, 1, 1))


class Plane(Shape):
    def __init__(self, transform=None, material=None):
        super().__init__(transform, material)

    def local_normal_at(self, point):
        return Vector(0, 1, 0)

    def local_intersect(self, ray):
        if abs(ray.direction.y) < 0.00001:
            return Intersections()
        return Intersections(Intersection(-ray.origin.y / ray.direction.y, self))

    def bounds(self):
        self.box = Bounds(minimum=Point(-float('inf'), 0, -float('inf')), maximum=Point(float('inf'), 0, float('inf')))


class Cube(Shape):
    def __init__(self, transform=None, material=None):
        super().__init__(transform, material)

    def local_intersect(self, ray):
        def check_axis(origin, direction):
            t_min_numerator = (-1 - origin)
            t_max_numerator = (1 - origin)
            t_min = t_min_numerator / direction if abs(direction) >= 0.00001 else t_min_numerator * float('inf')
            t_max = t_max_numerator / direction if abs(direction) >= 0.00001 else t_max_numerator * float('inf')
            if t_min > t_max:
                t_min, t_max = t_max, t_min

            return t_min, t_max

        x_t_min, x_t_max = check_axis(ray.origin.x, ray.direction.x)
        y_t_min, y_t_max = check_axis(ray.origin.y, ray.direction.y)
        z_t_min, z_t_max = check_axis(ray.origin.z, ray.direction.z)
        t_min = max(x_t_min, y_t_min, z_t_min)
        t_max = min(x_t_max, y_t_max, z_t_max)
        return Intersections(Intersection(t_min, self),
                             Intersection(t_max, self)) if t_min <= t_max else Intersections()

    def local_normal_at(self, point):
        max_c = max(abs(point.x), abs(point.y), abs(point.z))
        if max_c == abs(point.x):
            return Vector(point.x, 0, 0)
        elif max_c == abs(point.y):
            return Vector(0, point.y, 0)
        return Vector(0, 0, point.z)

    def bounds(self):
        self.box = Bounds(minimum=Point(-1, -1, -1), maximum=Point(1, 1, 1))


class Cylinder(Shape):
    def __init__(self, transform=None, material=None, minimum=None, maximum=None, closed=False):
        super().__init__(transform, material)
        self.minimum = -float('inf') if not minimum else minimum
        self.maximum = float('inf') if not maximum else maximum
        self.closed = closed

    def local_intersect(self, ray):
        xs = Intersections()
        a = ray.direction.x ** 2 + ray.direction.z ** 2
        if a >= 0.00001:
            b = 2 * ray.origin.x * ray.direction.x + 2 * ray.origin.z * ray.direction.z
            c = ray.origin.x ** 2 + ray.origin.z ** 2 - 1
            disc = b ** 2 - 4 * a * c
            if disc < 0:
                return xs

            t0 = (-b - disc ** 0.5) / (2 * a)
            t1 = (-b + disc ** 0.5) / (2 * a)

            if t0 > t1:
                t0, t1 = t1, t0

            y0 = ray.origin.y + t0 * ray.direction.y
            if self.minimum < y0 < self.maximum:
                xs.append(Intersection(t0, self))
            y1 = ray.origin.y + t1 * ray.direction.y
            if self.minimum < y1 < self.maximum:
                xs.append(Intersection(t1, self))
        self.intersect_caps(ray, xs)
        return xs

    def intersect_caps(self, ray, xs):
        def check_cap(ray, t):
            x = ray.origin.x + t * ray.direction.x
            z = ray.origin.z + t * ray.direction.z
            return x ** 2 + z ** 2 <= 1

        if not self.closed or abs(ray.direction.y) < 0.00001:
            return xs
        t = (self.minimum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t):
            xs.append(Intersection(t, self))
        t = (self.maximum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t):
            xs.append(Intersection(t, self))

    def local_normal_at(self, point):
        dist = point.x ** 2 + point.z ** 2
        if dist < 1 and point.y >= self.maximum - 0.00001:
            return Vector(0, 1, 0)
        elif dist < 1 and point.y <= self.minimum + 0.00001:
            return Vector(0, -1, 0)
        else:
            return Vector(point.x, 0, point.z)

    def bounds(self):
        self.box = Bounds(minimum=Point(-1, self.minimum, -1), maximum=Point(1, self.maximum, 1))


class Cone(Shape):
    def __init__(self, transform=None, material=None, minimum=None, maximum=None, closed=False):
        super().__init__(transform, material)
        self.minimum = -float('inf') if not minimum else minimum
        self.maximum = float('inf') if not maximum else maximum
        self.closed = closed

    def local_intersect(self, ray):
        xs = Intersections()
        a = ray.direction.x ** 2 - ray.direction.y ** 2 + ray.direction.z ** 2
        b = 2 * ray.origin.x * ray.direction.x - 2 * ray.origin.y * ray.direction.y + 2 * ray.origin.z * ray.direction.z
        c = ray.origin.x ** 2 - ray.origin.y ** 2 + ray.origin.z ** 2
        if abs(a) >= 0.00001:
            disc = b ** 2 - 4 * a * c
            if disc < 0:
                return xs

            t0 = (-b - disc ** 0.5) / (2 * a)
            t1 = (-b + disc ** 0.5) / (2 * a)

            if t0 > t1:
                t0, t1 = t1, t0

            y0 = ray.origin.y + t0 * ray.direction.y
            if self.minimum < y0 < self.maximum:
                xs.append(Intersection(t0, self))
            y1 = ray.origin.y + t1 * ray.direction.y
            if self.minimum < y1 < self.maximum:
                xs.append(Intersection(t1, self))
        else:
            if abs(b) >= 0.00001:
                xs.append(Intersection(-c / (2 * b), self))
        self.intersect_caps(ray, xs)
        return xs

    def intersect_caps(self, ray, xs):
        def check_cap(ray, t, y):
            x = ray.origin.x + t * ray.direction.x
            z = ray.origin.z + t * ray.direction.z
            return x ** 2 + z ** 2 <= y ** 2

        if not self.closed or abs(ray.direction.y) < 0.00001:
            return xs
        t = (self.minimum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t, self.minimum):
            xs.append(Intersection(t, self))
        t = (self.maximum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t, self.maximum):
            xs.append(Intersection(t, self))

    def local_normal_at(self, point):
        dist = point.x ** 2 + point.z ** 2
        if dist < 1 and point.y >= self.maximum - 0.00001:
            return Vector(0, 1, 0)
        elif dist < 1 and point.y <= self.minimum + 0.00001:
            return Vector(0, -1, 0)
        else:
            y = (point.x ** 2 + point.z ** 2) ** 0.5
            if point.y > 0:
                y = -y
            return Vector(point.x, y, point.z)

    def bounds(self):
        self.box = Bounds(minimum=Point(-1, self.minimum, -1), maximum=Point(1, self.maximum, 1))
