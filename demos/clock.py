import math

from features.canvas import Canvas
from features.matrix import Rotation
from features.tuple import Point, Color


if __name__ == "__main__":
    HOUR_ROTATION = math.pi / 6
    CANVAS_SIZE = 80
    RADIUS = 30

    twelve = Point(0, 0, 1)
    c = Canvas(80, 80)
    color = Color(1, 1, 1)

    for hour in range(12):
        p = Rotation(0, hour * HOUR_ROTATION, 0) * twelve
        x = int(p.x * RADIUS) + 40
        y = int(p.z * RADIUS) + 40
        c.write_pixel(x, y, color)

    with open("../images/clock.ppm", "w") as ppm_file:
        ppm_file.write(c.to_ppm())
