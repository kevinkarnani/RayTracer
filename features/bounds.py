from features.intersection import Intersection, Intersections
from features.tuple import Point


class Bounds:
    def __init__(self, minimum=None, maximum=None):
        self.minimum = Point(-float('inf'), -float('inf'), -float('inf')) if not minimum else minimum
        self.maximum = Point(float('inf'), float('inf'), float('inf')) if not maximum else maximum

    def add_point(self, point):
        self.minimum.x = min(self.minimum.x, point.x)
        self.minimum.y = min(self.minimum.y, point.y)
        self.minimum.z = min(self.minimum.z, point.z)
        self.maximum.x = max(self.maximum.x, point.x)
        self.maximum.y = max(self.maximum.y, point.y)
        self.maximum.z = max(self.maximum.z, point.z)

    def __add__(self, other):
        self.add_point(other.minimum)
        self.add_point(other.maximum)

    def contains_point(self, point):
        return self.minimum <= point <= self.maximum

    def contains_box(self, box):
        return self.contains_point(box.minumim) and self.contains_point(box.maximum)

    def transform(self, t):
        points = [self.minimum, Point(self.minimum.x, self.minimum.y, self.maximum.z),
                  Point(self.minimum.x, self.maximum.y, self.minimum.z),
                  Point(self.minimum.x, self.maximum.y, self.maximum.z),
                  Point(self.maximum.x, self.minimum.y, self.minimum.z),
                  Point(self.maximum.x, self.minimum.y, self.maximum.z),
                  Point(self.maximum.x, self.maximum.y, self.minimum.z), self.maximum]
        box = Bounds()

        for point in points:
            box.add_point(t * point)
        return box

    def intersect(self, ray):
        def check_axis(origin, direction, minimum, maximum):
            t_min_numerator = (minimum - origin)
            t_max_numerator = (maximum - origin)
            t_min = t_min_numerator / direction if abs(direction) >= 0.00001 else t_min_numerator * float('inf')
            t_max = t_max_numerator / direction if abs(direction) >= 0.00001 else t_max_numerator * float('inf')
            if t_min > t_max:
                t_min, t_max = t_max, t_min
            return t_min, t_max

        x_t_min, x_t_max = check_axis(ray.origin.x, ray.direction.x, self.minimum.x, self.maximum.x)
        y_t_min, y_t_max = check_axis(ray.origin.y, ray.direction.y, self.minimum.y, self.maximum.y)
        z_t_min, z_t_max = check_axis(ray.origin.z, ray.direction.z, self.minimum.z, self.maximum.z)
        t_min = max(x_t_min, y_t_min, z_t_min)
        t_max = min(x_t_max, y_t_max, z_t_max)
        return Intersections(Intersection(t_min, self),
                             Intersection(t_max, self)) if t_min <= t_max else Intersections()
