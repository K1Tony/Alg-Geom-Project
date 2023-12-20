from Shapes.Point import Point
from Assets.Color import Color
import math


class Line:
    def __init__(self, start: Point, end: Point, color: tuple[int, int, int] = Color.RED, width: int = 2):
        self.__start = min(start, end)
        self.__end = max(start, end)
        self.__color = color
        self.__width = width
        if start.x == end.x:
            self.__a = math.inf
        else:
            self.__a = (end.y - start.y) / (end.x - start.x)
        self.__b = start.y - start.x * self.__a

    def __str__(self):
        return f'{self.start, self.end}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Line):
            return self.start == other.start and self.end == other.end
        return False

    def __contains__(self, point: Point):
        """
        Function that checks if a point is contained in the line. Use the 'in' keyword to check.
        Example: line = ((1, 0), (4, 0)), pointA = (2, 0), pointB = (5, 0):
            pointA in line -> True; pointB in line -> False
        :param point: point to be checked if the line contains it
        :return: True if the point is inside the line, False otherwise
        """
        return abs(point.y - point.x * self.a - self.b) <= 10 ** -14 and \
    self.start.x <= point.x <= self.end.x and min(self.start.y, self.end.y) <= point.y <= max(self.start.y, self.end.y)

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def color(self):
        return self.__color

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def width(self):
        return self.__width

    @color.setter
    def color(self, color: tuple[int, int, int]):
        self.__color = color

    def y(self, x):
        if math.isinf(self.a):
            return math.inf

        return self.a * x + self.b

    def tuple(self):
        return self.start.tuple(), self.end.tuple()