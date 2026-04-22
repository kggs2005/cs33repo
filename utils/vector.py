from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2D:
    """Helper class representing two quantities: one for the x-axis and one for the y-axis."""
    x: int
    y: int

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def magnitude2(self) -> int:
        return self.x**2 + self.y**2

    def dot(self, other: Vector2D) -> int:
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: Vector2D) -> int:
        return self.x * other.y - self.y * other.x