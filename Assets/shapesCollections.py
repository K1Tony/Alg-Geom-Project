from abc import ABC
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Rectangle import Rectangle


class Collection(ABC):
    def __init__(self, items: list[Point] | list[Line] | list[Rectangle] = None, color: tuple[int, int, int] = None):
        self.__items = [] if items is None else items
        self.__color = color
        if color is not None:
            self.__items = list(map(lambda item: self.__change_color(item), self.__items))

    def __add__(self, other):
        if other is None: return self
        return self.__class__(self.items + other.items)

    def __sub__(self, other):
        if other is None: return self
        return self.__class__(list(set(self.items).difference(set(other.items))))

    def __getitem__(self, item):
        return self.__items[item]

    def __setitem__(self, key, value):
        self.__items[key] = value

    def __copy__(self):
        return self.__class__(list(map(lambda item: item.__copy__(), self.__items)))

    def index(self, value):
        return self.__items.index(value)

    def __change_color(self, item):
        item.color = self.__color
        return item

    def __len__(self):
        return len(self.__items)

    @property
    def items(self):
        return self.__items

    @property
    def color(self):
        return self.__color


class PointsCollection(Collection):
    def __init__(self, points: list[Point] = None, color: tuple[int, int, int] = None):
        super(PointsCollection, self).__init__(points, color)


class LinesCollection(Collection):
    def __init__(self, lines: list[Line] = None, color: tuple[int, int, int] = None):
        super(LinesCollection, self).__init__(lines, color)


class RectsCollection(Collection):
    def __init__(self, rects: list[Rectangle] = None, color: tuple[int, int, int] = None, alpha: int = None):
        super(RectsCollection, self).__init__(rects, color)
        self.__alpha = alpha

    @property
    def alpha(self):
        return self.__alpha
