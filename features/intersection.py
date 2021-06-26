import numpy as np


class Intersection(np.ndarray):
    def __new__(cls, t_values, obj):
        self = t_values.T.view(cls)
        self.obj = obj
        return self

    def __eq__(self, other):
        return np.allclose(self, other)

    @property
    def count(self):
        return self.shape[0]

    def hit(self):
        return self.min(axis=1) if self.shape[0] else None
