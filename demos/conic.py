import numpy as np

from features.camera import Camera
from features.light import Light
from features.material import Material
from features.matrix import Translation, Scaling, view_transform, Rotation
from features.pattern import Checker
from features.shape import Plane, Cone, Cylinder
from features.tuple import Color, Point, Vector
from features.world import World

if __name__ == "__main__":
    world = World()

    floor = Plane()
    floor.material = Material(pattern=Checker(Color(1, 1, 1), Color(0, 0, 0)), reflective=0.3, diffuse=0.9, specular=0)
    world.objects.append(floor)

    c1 = Cylinder(minimum=-1, maximum=1)
    c1.set_transform(Translation(-0.5, 1, 0.5) * Rotation(0, 0, np.pi / 6))
    c1.material.color = Color(0.8, 0.1, 0.1)
    world.objects.append(c1)

    c2 = Cone(minimum=-1, maximum=1)
    c2.set_transform(Translation(1.5, 0.5, -0.5) * Rotation(0, -np.pi / 6, 0) * Scaling(0.5, 0.5, 0.5))
    c2.material.color = Color(0, 0, 0.4)
    c2.material.diffuse = 0
    c2.material.specular = 1
    c2.material.reflective = 0.5
    c2.material.refractive_index = 1.5
    world.objects.append(c2)

    c3 = Cylinder(minimum=-1, maximum=1)
    c3.set_transform(Translation(-1.5, 0.33, -0.75) * Scaling(0.33, 0.33, 0.33))
    c3.material.color = Color(0, 0.4, 0)
    c3.material.diffuse = 0
    c3.material.specular = 1
    c3.material.refractive_index = 1.5
    world.objects.append(c3)

    world.light = Light(Point(10, 10, -10), Color(1, 1, 1))
    camera = Camera(1000, 500, np.pi / 3)
    camera.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)

    with open("../images/conic.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
