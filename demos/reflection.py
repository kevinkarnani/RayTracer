import numpy as np

from features.camera import Camera
from features.light import Light
from features.matrix import Scaling, Translation, view_transform
from features.pattern import Checker, Ring, Gradient, Stripe
from features.shape import Sphere, Plane
from features.tuple import Color, Point, Vector
from features.world import World

if __name__ == "__main__":
    world = World()

    floor = Plane()
    floor.material.specular = 0
    floor.material.pattern = Checker(Color(1, 0.9, 0.9), Color(0, 0.1, 0.1))
    floor.material.reflective = 0.5
    world.objects.append(floor)

    middle = Sphere.glassy()
    middle.set_transform(Translation(-0.5, 1, 0.5))
    middle.material.pattern = Ring(Color(0.1, 1, 0.5), Color(0.9, 0, 0.5))
    middle.material.pattern.set_transform(Scaling(0.1, 0.1, 0.1))
    middle.material.reflective = 1
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    world.objects.append(middle)

    right = Sphere()
    right.set_transform(Translation(1.5, 0.5, -0.5) * Scaling(0.5, 0.5, 0.5))
    right.material.pattern = Gradient(Color(0.5, 1, 0.1), Color(0.5, 0, 0.9))
    right.material.pattern.set_transform(Scaling(0.5, 0.5, 0.5))
    right.material.transparency = 0.5
    right.material.diffuse = 0.7
    right.material.specular = 0.3
    right.material.reflective = 0.5
    right.material.refractive_index = 2
    world.objects.append(right)

    left = Sphere()
    left.set_transform(Translation(-1.5, 0.33, -0.75) * Scaling(0.33, 0.33, 0.33))
    left.material.pattern = Stripe(Color(1, 0.8, 0.1), Color(0, 0.2, 0.9))
    left.material.pattern.set_transform(Scaling(0.1, 0.1, 0.1))
    left.material.transparency = 0
    left.material.diffuse = 0.7
    left.material.specular = 0.3
    left.material.reflective = 1
    left.material.refractive_index = 0.5
    world.objects.append(left)

    world.light = Light(Point(-10, 10, -10), Color(1, 1, 1))
    camera = Camera(800, 400, np.pi / 3)
    camera.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)

    with open("../images/reflection.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
