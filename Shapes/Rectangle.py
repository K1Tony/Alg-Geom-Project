from pygame import Rect
from Assets.Color import Color
from Shapes.Point import Point


class Rectangle:

    def __init__(self, top: float = 0, left: float = 0, width: float = 0, height: float = 0,
                 fill_color: tuple[int, int, int] = Color.VOID, border_width: int = 3,
                 border_color: tuple[int, int, int] = Color.RED,
                 alpha: int = 255):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.right = self.left + self.width
        self.bottom = self.top + self.height

        self.topleft = self.left, self.top
        self.topright = self.right, self.top
        self.bottomleft = self.left, self.bottom
        self.bottomright = self.right, self.bottom

        self.size = width, height
        self.color = fill_color
        self.border_width = border_width
        self.border_color = border_color
        self.alpha = alpha

    def __contains__(self, item):
        if isinstance(item, tuple):
            return self.left <= item[0] <= self.right \
                   and self.top <= item[1] <= self.bottom
        if isinstance(item, Point):
            return item.tuple() in self

        if isinstance(item, Rectangle):
            return self.left <= item.left and self.top <= item.top and\
                   self.right >= item.right and\
                self.bottom >= item.bottom
        return False

    def __copy__(self):
        return Rectangle(self.top, self.left, self.width, self.height, self.color, self.border_width,
                         self.border_color, self.alpha)

    @staticmethod
    def form(point1: Point, point2: Point, **kwargs):
        top = min(point1, point2, key=lambda point: point.y).y
        left = min(point1, point2).x
        bot = max(point1, point2, key=lambda point: point.y).y
        right = max(point1, point2).x
        return Rectangle(top, left, right - left, bot - top, **kwargs)

    def colliderect(self, other: "Rectangle"):
        return (self.right >= other.left and self.top <= other.bottom and self.bottom >= other.top)\
    or (self.left <= other.right and self.top <= other.bottom and self.bottom >= other.top)\
    or (self.top <= other.bottom and self.left <= other.right and self.right >= other.left)\
    or (self.bottom >= other.top and self.left <= other.right and self.right >= other.left)
