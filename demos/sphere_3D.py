from features.canvas import Canvas
from features.light import Light
from features.material import Material
from features.ray import Ray
from features.shape import Sphere
from features.tuple import Color, Point

if __name__ == "__main__":
    WALL_SIZE = 7
    CANVAS_SIZE = 1000
    PIXEL_SIZE = WALL_SIZE / CANVAS_SIZE
    HALF = WALL_SIZE / 2

    canvas = Canvas(CANVAS_SIZE, CANVAS_SIZE)
    s = Sphere()
    m = Material(color=Color(1, 0.2, 1))
    s.material = m

    light = Light(Point(-10, 5, -10), Color(1, 1, 1))
    ray_origin = Point(0, 0, -5)
    wall_z = 10

    for y in range(0, CANVAS_SIZE):
        world_y = HALF - PIXEL_SIZE * y
        for x in range(0, CANVAS_SIZE):
            world_x = -HALF + PIXEL_SIZE * x
            position = Point(world_x, world_y, wall_z)
            v = position - ray_origin
            r = Ray(ray_origin, v.normalize())
            xs = s.intersect(r)
            hit = xs.hit()
            if hit:
                point = r.position(hit.t)
                normal = hit.obj.normal_at(point)
                eye = -r.direction
                c = hit.obj.material.lighting(hit.obj, light, point, eye, normal)
                canvas.write_pixel(x, y, c)

    with open("../images/sphere_3D.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
