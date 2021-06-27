import numpy as np

from features.camera import Camera
from features.light import Light
from features.material import Material
from features.matrix import Scaling, Translation, Rotation, view_transform
from features.shape import Sphere
from features.tuple import Color, Point, Vector
from features.world import World

if __name__ == "__main__":
    world = World()

    floor = Sphere()
    floor.set_transform(Scaling(10, 0.01, 10))
    floor.material = Material()
    floor.material.color = Color(1, 0.9, 0.9)
    floor.material.specular = 0
    world.objects.append(floor)

    left_wall = Sphere()
    left_wall.set_transform(Translation(0, 0, 5) * Rotation(np.pi / 2, -np.pi / 4, 0) * Scaling(10, 0.01, 10))
    left_wall.material = floor.material
    world.objects.append(left_wall)

    right_wall = Sphere()
    right_wall.set_transform(Translation(0, 0, 5) * Rotation(np.pi / 2, np.pi / 4, 0) * Scaling(10, 0.01, 10))
    right_wall.material = floor.material
    world.objects.append(right_wall)

    middle = Sphere()
    middle.set_transform(Translation(-0.5, 1, 0.5))
    middle.material.color = Color(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    world.objects.append(middle)

    right = Sphere()
    right.set_transform(Translation(1.5, 0.5, -0.5) * Scaling(0.5, 0.5, 0.5))
    right.material.color = Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3
    world.objects.append(right)

    left = Sphere()
    left.set_transform(Translation(-1.5, 0.33, -0.75) * Scaling(0.33, 0.33, 0.33))
    left.material.color = Color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3
    world.objects.append(left)

    world.light = Light(Point(-10, 10, -10), Color(1, 1, 1))
    camera = Camera(1000, 500, np.pi / 3)
    camera.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    canvas = camera.render(world)

    with open("../images/world_and_shadow.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
