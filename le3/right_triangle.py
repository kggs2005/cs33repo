from utils.vector import Vector2D


def is_right_triangle(p1: Vector2D, p2: Vector2D, p3: Vector2D) -> bool:
    """Returns True if 3 points make up a right triangle, and False otherwise."""
    if (p2 - p1).cross(p3 - p1) == 0:
        return False
    elif (p2 - p1).dot(p3 - p1) == 0 or (p1 - p2).dot(p3 - p2) == 0 or (p1 - p3).dot(p2 - p3) == 0:
        return True
    else:
        return False