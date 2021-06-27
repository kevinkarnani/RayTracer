import numpy as np


class Intersection:
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj

    def __eq__(self, other):
        return isinstance(other, Intersection) and self.t == other.t and self.obj == self.obj

    def __lt__(self, other):
        return isinstance(other, Intersection) and self.t < other.t and self.obj == self.obj

    def prepare_computations(self, r, xs=None):
        comps = Computations(self.t, self.obj)
        comps.point = r.position(comps.t)
        comps.eye_v = -r.direction
        comps.normal_v = comps.obj.normal_at(comps.point)
        comps.inside = False

        if comps.normal_v.dot(comps.eye_v) < 0:
            comps.inside = True
            comps.normal_v = -comps.normal_v

        comps.n1 = comps.n2 = 1

        if xs:
            containers = []
            for i in xs:
                if i == self:
                    comps.n1 = 1 if not (len(containers)) else containers[len(containers) - 1].material.refractive_index

                if i.obj in containers:
                    containers.remove(i.obj)
                else:
                    containers.append(i.obj)

                if i == self:
                    comps.n2 = 1 if not (len(containers)) else containers[len(containers) - 1].material.refractive_index

        comps.over_point = comps.point + comps.normal_v * 0.00001
        comps.under_point = comps.point - comps.normal_v * 0.00001
        comps.reflect_v = r.direction.reflect(comps.normal_v)
        return comps


class Computations:
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj
        self.point = None
        self.eye_v = None
        self.normal_v = None
        self.inside = None
        self.over_point = None
        self.under_point = None
        self.reflect_v = None
        self.n1 = None
        self.n2 = None

    def schlick(self):
        cos = self.eye_v.dot(self.normal_v)

        if self.n1 > self.n2:
            n = self.n1 / self.n2
            sin2_t = n ** 2 * (1 - cos ** 2)
            if sin2_t > 1:
                return 1

            cos = np.sqrt(1 - sin2_t)

        r0 = ((self.n1 - self.n2) / (self.n1 + self.n2)) ** 2
        return r0 + (1 - r0) * (1 - cos) ** 5


class Intersections(list):
    def __init__(self, *args):
        super(Intersections, self).__init__(args)
        self.count = len(args)

    def hit(self):
        return min([i for i in self if i.t > 0], default=None)
