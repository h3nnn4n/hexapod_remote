import typing as t
from math import atan2, cos, sin
from random import uniform


class Vector3d:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "%f %f %f" % (self.x, self.y, self.z)

    def __repr__(self):
        return "%f %f %f" % (self.x, self.y, self.z)


class Vector:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Vector") -> "Vector":
        self = Vector(self.x + other.x, self.y + other.y)
        return self

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other: "Vector") -> "Vector":
        self = Vector(self.x - other.x, self.y - other.y)
        return self

    def __mul__(self, other: "Vector") -> "Vector":
        return Vector(self.x * other.x, self.y * other.y)

    def __imul__(self, other: "Vector") -> "Vector":
        self = Vector(self.x * other.x, self.y * other.y)
        return self

    def __str__(self):
        return "%f %f" % (self.x, self.y)

    def __repr__(self):
        return "%f %f" % (self.x, self.y)

    def normalize(self) -> "Vector":
        self.data = self.data / self.norm

        return self

    @property
    def heading(self) -> float:
        return atan2(self.y, self.x)

    @property
    def norm(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    @property
    def as_tuple(self) -> t.Tuple[float, float]:
        return self.x, self.y

    def dist(self, other):
        return other.copy().__sub__(self).norm

    def limit(self, mag):
        if self.norm > mag:
            self.set_mag(mag)

        return self

    def set_mag(self, mag):
        self.normalize()
        t = self * mag
        self.x = t.x
        self.y = t.y
        return self

    def zero(self):
        self.x = 0
        self.y = 0

        return self

    def from_angle(self, angle: float, length: float = 1.0) -> "Vector":
        self.x = length * cos(angle)
        self.y = length * sin(angle)

        return self

    def random(self):
        self.x = uniform(-1, 1)
        self.y = uniform(-1, 1)

        return self

    def rotate(self, angle: float) -> "Vector":
        self.x = self.x * cos(angle) - self.y * sin(angle)
        self.y = self.x * sin(angle) + self.y * cos(angle)

        return self

    def copy(self):
        return Vector(self.x, self.y)
