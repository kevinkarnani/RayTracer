import numpy as np

from features.camera import Camera
from features.group import Hexagon
from features.light import Light
from features.material import Material
from features.matrix import Translation, Scaling, view_transform, Rotation
from features.pattern import Checker
from features.shape import Plane
from features.tuple import Color, Point, Vector
from features.world import World

if __name__ == "__main__":
    world = World()

    floor = Plane()
    floor.set_transform(Translation(0, -1, 0))
    floor.material = Material(pattern=Checker(Color(1, 1, 1), Color(0, 0, 0)), reflective=0.5, specular=0)
    world.objects.append(floor)

    h1 = Hexagon().create()
    h1.set_transform(Translation(-0.5, 1, 0.5) * Rotation(0, np.pi / 6, np.pi / 4))
    h1.material.color = Color(0.8, 0.1, 0.1)
    h1.set_material()
    world.objects.append(h1)

    world.light = Light(Point(10, 10, -10), Color(1, 1, 1))
    camera = Camera(1000, 500, np.pi / 3)
    camera.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)

    with open("../images/group.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
