

class Point:
    def __init__(self, x: float, y: float, radius: float, color: tuple[int, int, int] = (255, 0, 0)):
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__color = color

    def __str__(self):
        return f'{self.x, self.y}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __lt__(self, other):
        if isinstance(other, Point):
            return min(self, other, key=lambda point: (point.x, point.y)) is self
        raise TypeError()

    def __hash__(self):
        return self.x.__hash__() * self.y.__hash__()

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def pos(self):
        return self.x, self.y

    @property
    def radius(self):
        return self.__radius

    @property
    def diameter(self):
        return self.__radius + self.__radius

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color: tuple[int, int, int]):
        self.__color = new_color

    def tuple(self):
        return self.x, self.y
