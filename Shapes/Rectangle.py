from pygame import Rect
from Assets.Color import Color
from Shapes.Point import Point


class Rectangle(Rect):

    __EPS = 10 ** -12

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
            return self.x - self.__EPS <= item[0] <= self.x + self.width + self.__EPS\
                   and self.y - self.__EPS <= item[1] <= self.y + self.height + self.__EPS
        if isinstance(item, Point):
            return item.tuple() in self

        if isinstance(item, Rectangle):
            return self.x - self.__EPS <= item.x and self.y - self.__EPS <= item.y and\
                   self.x + self.width + self.__EPS >= item.x + item.width and\
                self.y + self.height + self.__EPS >= item.y + item.height
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
