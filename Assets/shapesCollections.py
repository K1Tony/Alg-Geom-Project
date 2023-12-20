from abc import ABC, abstractmethod
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Rectangle import Rectangle


class Collection(ABC):
    def __init__(self, items: list[Point] | list[Line] | list[Rectangle] = None, color: tuple[int, int, int] = None):
        self.__items = [] if items is None else items
        self.__color = color
        if color is not None:
            self.__items = list(map(lambda item: self.__change_color(item), self.__items))

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    def __getitem__(self, item):
        return self.__items[item]

    def __setitem__(self, key, value):
        self.__items[key] = value

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

    def __add__(self, other):
        if other is None: return self
        return PointsCollection(self.items + other.items)

    def __sub__(self, other):
        if other is None: return self
        return PointsCollection(list(set(self.items).difference(set(other.items))))


class LinesCollection(Collection):
    def __init__(self, lines: list[Line] = None, color: tuple[int, int, int] = None):
        super(LinesCollection, self).__init__(lines, color)

    def __add__(self, other):
        if other is None: return self
        return LinesCollection(self.items + other.items)

    def __sub__(self, other):
        if other is None: return self
        return LinesCollection(list(set(self.items).difference(set(other.items))))


class RectsCollection(Collection):
    def __init__(self, rects: list[Rectangle] = None, color: tuple[int, int, int] = None, alpha: int = None):
        super(RectsCollection, self).__init__(rects, color)
        self.__alpha = alpha

    def __add__(self, other):
        if other is None: return self
        return RectsCollection(self.items + other.items)

    def __sub__(self, other):
        if other is None: return self
        return RectsCollection(list(set(self.items).difference(set(other.items))))

    @property
    def alpha(self):
        return self.__alpha
