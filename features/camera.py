import numpy as np

from features.canvas import Canvas
from features.matrix import Matrix
from features.ray import Ray
from features.tuple import Point


class Camera:
    def __init__(self, h_size, v_size, fov, transform=None):
        self.h_size = h_size
        self.v_size = v_size
        self.fov = fov
        self.transform = Matrix.identity(4) if not transform else transform

        half_view = np.tan(self.fov / 2)
        aspect = self.h_size / self.v_size

        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view

        self.pixel_size = (self.half_width * 2) / self.h_size

    def ray_for_pixel(self, x, y):
        x_offset = (x + 0.5) * self.pixel_size
        y_offset = (y + 0.5) * self.pixel_size

        pixel = self.transform.inverse() * Point(self.half_width - x_offset, self.half_height - y_offset, -1)
        origin = self.transform.inverse() * Point(0, 0, 0)
        return Ray(origin, (pixel - origin).normalize())

    def render(self, world):
        image = Canvas(self.h_size, self.v_size)

        for y in range(self.v_size):
            for x in range(self.h_size):
                image.write_pixel(x, y, world.color_at(self.ray_for_pixel(x, y)))
        return image
