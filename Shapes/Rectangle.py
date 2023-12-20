from pygame import Rect
from Assets.Color import Color
from Shapes.Point import Point


class Rectangle(Rect):
    def __init__(self, top: float = 0, left: float = 0, width: float = 0, height: float = 0,
                 fill_color: tuple[int, int, int] = Color.VOID, border_width: int = 3,
                 border_color: tuple[int, int, int] = Color.RED,
                 alpha: int = 255):
        super(Rectangle, self).__init__(left, top, width, height)
        self.color = fill_color
        self.border_width = border_width
        self.border_color = border_color
        self.alpha = alpha

    def __contains__(self, item):
        if isinstance(item, tuple):
            return self.x <= item[0] <= self.x + self.width and self.y <= item[1] <= self.y + self.height
        if isinstance(item, Point):
            return self.x <= item.x - item.radius and item.x + item.radius <= self.x + self.width and\
                   self.y <= item.y - item.radius and item.y + item.radius <= self.x + self.height
        if isinstance(item, Rectangle):
            return self.x <= item.x and self.y <= item.y and self.x + self.width >= item.x + item.width and\
                self.y + self.height >= item.y + item.height
        return False

    @staticmethod
    def form(point1: Point, point2: Point, **kwargs):
        top = min(point1, point2, key=lambda point: point.y).y
        left = min(point1, point2).x
        bot = max(point1, point2, key=lambda point: point.y).y
        right = max(point1, point2).x
        return Rectangle(top, left, right - left, bot - top, **kwargs)
