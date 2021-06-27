import numpy as np

from features.tuple import Color


class Material:
    def __init__(self, color=Color(1, 1, 1), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.pattern = None

    def __eq__(self, other):
        return self.color == other.color and self.ambient == other.ambient and self.diffuse == other.diffuse and \
               self.specular == other.specular and self.shininess == other.shininess

    def lighting(self, obj, light, point, eye, normal, in_shadow=False):
        color = self.color if not self.pattern else self.pattern.stripe_at_object(obj, point)
        diffuse = Color(0, 0, 0)
        specular = Color(0, 0, 0)
        effective_color = color * light.intensity
        light_v = (light.position - point).normalize()
        ambient = effective_color * self.ambient
        if in_shadow:
            return ambient

        light_dot_normal = light_v.dot(normal)

        if light_dot_normal >= 0:
            diffuse = effective_color * self.diffuse * light_dot_normal
            reflect_v = -light_v.reflect(normal)
            reflect_dot_eye = reflect_v.dot(eye)

            if reflect_dot_eye >= 0:
                factor = np.power(reflect_dot_eye, self.shininess)
                specular = light.intensity * self.specular * factor

        return ambient + diffuse + specular
