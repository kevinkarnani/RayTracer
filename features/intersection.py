class Intersection:
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj

    def __eq__(self, other):
        return isinstance(other, Intersection) and self.t == other.t and self.obj == self.obj

    def __lt__(self, other):
        return isinstance(other, Intersection) and self.t < other.t and self.obj == self.obj

    def prepare_computations(self, r):
        comps = Computations(self.t, self.obj)
        comps.point = r.position(comps.t)
        comps.eye_v = -r.direction
        comps.normal_v = comps.obj.normal_at(comps.point)
        comps.inside = False

        if comps.normal_v.dot(comps.eye_v) < 0:
            comps.inside = True
            comps.normal_v = -comps.normal_v

        return comps


class Computations:
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj
        self.point = None
        self.eye_v = None
        self.normal_v = None
        self.inside = None


class Intersections(list):
    def __init__(self, *args):
        super(Intersections, self).__init__(args)
        self.count = len(args)

    def hit(self):
        return min([i for i in self if i.t > 0], default=None)
