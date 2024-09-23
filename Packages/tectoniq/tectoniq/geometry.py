from math import cos, sin, sqrt

from shapely.geometry import Point

def add(point1: Point, point2: Point) -> Point:
    return Point(point1.x + point2.x, point1.y + point2.y)

def distance(point1: Point, point2: Point) -> float:
    """Returns the 2D Euclidean distance between two points."""
    return sqrt(pow(point1.x - point2.x, 2.0) + pow(point1.y - point2.y, 2.0))

def distance_to_line(point1: Point, point2: Point, angle: float) -> float:
    """Returns a distance measure representing the distance from a line going through one of the points at an angle measured anti-clockwise from the positive x-axis."""
    return abs(-(sin(angle) * point1.x) + (cos(angle) * point1.y) + (sin(angle) * point2.x) - (cos(angle) * point2.y))

def distance_to_line_segment(point: Point, line_point1: Point, line_point2: Point) -> float:
    """Returns the shortest distance between a point and two points defining a line segment."""
    length_squared: float = pow(line_point1.x - line_point2.x, 2) + pow(line_point1.y - line_point2.y, 2)
    if length_squared == 0:
        # Not a line segment, just a point.
        return distance(point, line_point1)
    
    t: float = max(0, min(1, dot_product(subtract(point, line_point1), subtract(line_point2, line_point1)) / length_squared))

    projection: Point = add(line_point1, Point(t * subtract(line_point2, line_point1).x, t * subtract(line_point2, line_point1).y))

    return distance(point, projection)

def dot_product(point1: Point, point2: Point) -> float:
    return (point1.x * point2.x) + (point1.y * point2.y)

def negate(point: Point) -> Point:
    return Point(-point.x, -point.y)

def subtract(point1: Point, point2: Point) -> Point:
    return add(point1, negate(point2))

all = [distance, distance_to_line, distance_to_line_segment]