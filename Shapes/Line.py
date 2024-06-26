from Shapes.Point import Point
from Assets.Color import Color
import math


class Line:
    def __init__(self, start: Point, end: Point, color: tuple[int, int, int] = Color.RED, width: int = 2):
        self.__start = min(start, end)
        self.__end = max(start, end)
        self.__color = color
        self.__width = width

    def __str__(self):
        return f'{self.start, self.end}'

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return Line(self.start, self.end, self.color, self.width)

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
    def width(self):
        return self.__width

    @color.setter
    def color(self, color: tuple[int, int, int]):
        self.__color = color

    def tuple(self):
        return self.start.tuple(), self.end.tuple()
