class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, time):
        return self.origin + time * self.direction

    def transform(self, m):
        return Ray(m * self.origin, m * self.direction)

    def __str__(self):
        return f"Ray: {{Origin: {self.origin}, Direction: {self.direction}}}"
