from features.canvas import Canvas
from features.tuple import Point, Vector, Color


class World:
    def __init__(self, g, w):
        self.gravity = g
        self.wind = w


class Projectile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


def tick(world, p):
    pos = p.position + p.velocity
    velocity = p.velocity + world.gravity + world.wind
    return Projectile(pos, velocity)


if __name__ == "__main__":
    start = Point(0, 1, 0)
    vel = Vector(1, 1.8, 0).normalize() * 11.25
    p = Projectile(start, vel)
    gravity = Vector(0, -0.1, 0)
    wind = Vector(-0.01, 0, 0)
    w = World(gravity, wind)
    c = Canvas(900, 550)
    c1 = Color(1, 0, 0)
    t = 0

    while p.position.y > 0:
        c.write_pixel(int(p.position.x), int(550 - p.position.y), c1)
        p = tick(w, p)
        t = t + 1

    with open("../images/projectile.ppm", "w") as ppm_file:
        ppm_file.write(c.to_ppm())
