from features.canvas import Canvas
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Point, Color

if __name__ == "__main__":
    WALL_SIZE = 7
    CANVAS_SIZE = 100
    PIXEL_SIZE = WALL_SIZE / CANVAS_SIZE
    HALF = WALL_SIZE / 2

    canvas = Canvas(CANVAS_SIZE, CANVAS_SIZE)
    c = Color(1, 0, 0)
    s = Sphere()
    ray_origin = Point(0, 0, -5)
    wall_z = 10

    for y in range(CANVAS_SIZE):
        world_y = HALF - PIXEL_SIZE * y
        for x in range(0, CANVAS_SIZE):
            world_x = -HALF + PIXEL_SIZE * x
            position = Point(world_x, world_y, wall_z)
            v = position - ray_origin
            r = Ray(ray_origin, v.normalize())
            xs = s.intersect(r)
            if xs.hit():
                canvas.write_pixel(x, y, c)

    with open("../images/sphere.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())