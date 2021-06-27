import numpy as np

from features.camera import Camera
from features.light import Light
from features.material import Material
from features.matrix import Rotation, Translation, Scaling, view_transform
from features.pattern import Checker, Stripe
from features.shape import Plane, Cube
from features.tuple import Color, Point, Vector
from features.world import World

if __name__ == "__main__":
    world = World()

    wall_material = Material()
    wall_material.pattern = Stripe(Color(0.45, 0.45, 0.45), Color(0.55, 0.55, 0.55))
    wall_material.pattern.set_transform(Scaling(0.25, 0.25, 0.25) * Rotation(0, np.pi / 2, 0))
    wall_material.ambient = 0
    wall_material.diffuse = 0.4
    wall_material.specular = 0
    wall_material.reflective = 0.3

    floor = Plane()
    floor.set_transform(Rotation(0, np.pi / 10, 0))
    floor.material.pattern = Checker(Color(0.35, 0.35, 0.35), Color(0.65, 0.65, 0.65))
    floor.material.specular = 0
    floor.material.reflective = 0.4
    world.objects.append(floor)

    ceiling = Plane()
    ceiling.set_transform(Translation(0, 5, 0))
    ceiling.material.color = Color(0.8, 0.8, 0.8)
    ceiling.material.ambient = 0.3
    ceiling.material.specular = 0
    world.objects.append(ceiling)

    left_wall = Plane()
    left_wall.set_transform(Rotation(0, np.pi / 2, np.pi / 2) * Translation(-5, 0, 0))
    left_wall.material = wall_material
    world.objects.append(left_wall)

    right_wall = Plane()
    right_wall.set_transform(Rotation(0, np.pi / 2, np.pi / 2) * Translation(5, 0, 0))
    right_wall.material = wall_material
    world.objects.append(right_wall)

    north_wall = Plane()
    north_wall.set_transform(Rotation(np.pi / 2, 0, 0) * Translation(0, 0, 5))
    north_wall.material = wall_material
    world.objects.append(north_wall)

    south_wall = Plane()
    north_wall.set_transform(Rotation(np.pi / 2, 0, 0) * Translation(0, 0, -5))
    north_wall.material = wall_material
    world.objects.append(south_wall)

    red_box = Cube()
    red_box.set_transform(Translation(-0.6, 1, 0.6))
    red_box.material.color = Color(1, 0, 0)
    red_box.material.specular = 0.4
    red_box.material.shininess = 5
    world.objects.append(red_box)

    blue_glass_box = Cube()
    blue_glass_box.set_transform(Scaling(0.7, 0.7, 0.7) * Translation(0.6, 0.7, -0.6))
    blue_glass_box.material.color = Color(0, 0, 1)
    blue_glass_box.material.ambient = 0
    blue_glass_box.material.diffuse = 0.4
    blue_glass_box.material.specular = 0.9
    blue_glass_box.material.shininess = 300
    blue_glass_box.material.reflective = 0.9
    blue_glass_box.material.transparency = 0.9
    blue_glass_box.material.refractive_index = 1.5
    world.objects.append(blue_glass_box)

    world.light = Light(Point(-4.9, 4.9, -1), Color(1, 1, 1))
    camera = Camera(800, 400, np.pi / 3)
    camera.transform = view_transform(Point(-2.6, 1.5, -3.9), Point(-0.6, 1, -0.8), Vector(0, 1, 0))
    canvas = camera.render(world)

    with open("../images/cube.ppm", "w") as ppm_file:
        ppm_file.write(canvas.to_ppm())
