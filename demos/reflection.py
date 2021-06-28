import numpy as np

from features.camera import Camera
from features.light import Light
from features.material import Material
from features.matrix import Scaling, Translation, view_transform
from features.pattern import Checker
from features.shape import Sphere, Plane
from features.tuple import Color, Point, Vector
from features.world import World

if __name__ == "__main__":
    world = World()

    floor = Plane()
    floor.material.specular = 0
    floor.material.pattern = Checker(Color(1, 0.9, 0.9), Color(0, 0.1, 0.1))
    floor.material.reflective = 0.4
    world.objects.append(floor)

    material = Material(color=Color(1, 0.3, 0.2), specular=0.4, shininess=5, refractive_index=0.1)
    s1 = Sphere(transform=Translation(6, 1, 4), material=material)
    s2 = Sphere(transform=Translation(2, 1, 3), material=material)
    s3 = Sphere(transform=Translation(-1, 1, 2), material=material)
    world.objects.extend([s1, s2, s3])

    blue = Sphere(transform=Translation(0.6, 0.7, -0.6) * Scaling(0.7, 0.7, 0.7))
    blue.material = Material(color=Color(0, 0, 0.2))
    blue.material.ambient = 0
    blue.material.diffuse = 0.4
    blue.material.specular = 0.9
    blue.material.shininess = 300
    blue.material.reflective = 0.9
    blue.material.transparency = 0.9
    blue.material.refractive_index = 1.5
    world.objects.append(blue)

    green = Sphere(transform=Translation(-0.7, 0.5, -0.8) * Scaling(0.5, 0.5, 0.5))
    green.material = Material(color=Color(0, 0.2, 0))
    green.material.ambient = 0
    green.material.diffuse = 0.4
    green.material.specular = 0.9
    green.material.shininess = 300
    green.material.reflective = 0.9
    green.material.transparency = 0.3
    green.material.refractive_index = 3.5
    world.objects.append(green)

    world.light = Light(Point(-10, 10, -10), Color(1, 1, 1))
    camera = Camera(640, 400, np.pi / 3)
    camera.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)

    with open("../images/reflection.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
