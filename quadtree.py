import numpy as np
Point = tuple[float, float]
Line = tuple[Point, Point]

def generate_uniform_points(left, right, n = 10 ** 5):
    x = np.float64(np.random.uniform(low=left, high=right, size=n))
    y = np.float64(np.random.uniform(low=left, high=right, size=n))
    return list(zip(x, y))

class Interval:
    def __init__(self, left: float, right: float):
        self.left: float = left
        self.right: float = right

    def __contains__(self, item: float) -> bool:
        return self.left <= item <= self.right

    def mid(self):
        return 0.5 * (self.left + self.right)

    def lower_half(self):
        return Interval(self.left, self.mid())

    def upper_half(self):
        return Interval(self.mid(), self.right)

    def __str__(self):
        return f"[{self.left:.2f}, {self.right:.2f}]"

    def intersects(self, other: "Interval") -> bool:
        return self.right in other or other.right in self


class Rectangle:
    def __init__(self, intervalx, intervaly):
        self.intervalx: Interval = intervalx
        self.intervaly: Interval = intervaly

    def __contains__(self, item: Point) -> bool:
        return item[0] in self.intervalx and item[1] in self.intervaly

    def __str__(self):
        return f"{self.intervalx}x{self.intervaly}"

    @classmethod
    def boundary(cls, points: list[Point]) -> "Rectangle":
        minx = min(x for x, y in points)
        maxy = max(y for x, y in points)
        miny = min(y for x, y in points)
        maxx = max(x for x, y in points)
        return cls(Interval(minx, maxx), Interval(miny, maxy))

    @classmethod
    def from_tuples(cls, xs: tuple[float, float], ys: tuple[float, float]) -> "Rectangle":
        return cls(Interval(xs[0], xs[1]), Interval(ys[0], ys[1]))

    def NE(self):
        return Rectangle(self.intervalx.upper_half(), self.intervaly.upper_half())

    def NW(self):
        return Rectangle(self.intervalx.lower_half(), self.intervaly.upper_half())

    def SW(self):
        return Rectangle(self.intervalx.lower_half(), self.intervaly.lower_half())

    def SE(self):
        return Rectangle(self.intervalx.upper_half(), self.intervaly.lower_half())

    def intersects(self, other: "Rectangle") -> bool:
        return self.intervalx.intersects(other.intervalx) and self.intervaly.intersects(other.intervaly)

    def vertices(self) -> list[Point]:
        NE = (self.intervalx.right, self.intervaly.right)
        NW = (self.intervalx.left, self.intervaly.right)
        SW = (self.intervalx.left, self.intervaly.left)
        SE = (self.intervalx.right, self.intervaly.left)
        return [NE, NW, SW, SE]

    def edges(self) -> list[Line]:
        NE, NW, SW, SE = self.vertices()
        return [(NE, NW),
                (NW, SW),
                (SW, SE),
                (SE, NE)
                ]


class Node:
    def __init__(self, rect, points, parent=None):
        self.rect = rect
        self.points = points
        self.parent = parent
        self.NE = None
        self.NW = None
        self.SW = None
        self.SE = None

    def _divide(self):
        xmid = self.rect.intervalx.mid()
        ymid = self.rect.intervaly.mid()
        PNE = [p for p in self.points if p[0] > xmid and p[1] > ymid]
        PNW = [p for p in self.points if p[0] <= xmid and p[1] > ymid]
        PSW = [p for p in self.points if p[0] <= xmid and p[1] <= ymid]
        PSE = [p for p in self.points if p[0] > xmid and p[1] <= ymid]

        self.NE = Node(self.rect.NE(), PNE, self)
        self.NW = Node(self.rect.NW(), PNW, self)
        self.SW = Node(self.rect.SW(), PSW, self)
        self.SE = Node(self.rect.SE(), PSE, self)
        self.points = None

    def _divide_recursively(self):
        if len(self.points) < 2:
            return
        self._divide()

        self.NE._divide_recursively()
        self.NW._divide_recursively()
        self.SW._divide_recursively()
        self.SE._divide_recursively()

    def __str__(self):
        return f"Node({self.rect}, {self.points})"

    def is_leaf(self):
        return self.NE is None

    def stringify(self, level=0):
        if self.is_leaf():
            return level * "  " + str(self)
        else:
            NEstr = self.NE.stringify(level + 1)
            NWstr = self.NW.stringify(level + 1)
            SWstr = self.SW.stringify(level + 1)
            SEstr = self.SE.stringify(level + 1)
            return level * "  " + f"{self}\n{NEstr}\n{NWstr}\n{SWstr}\n{SEstr}"

    def _search(self, rect) -> list[Point]:
        if not self.rect.intersects(rect):
            return []
        if self.is_leaf():
            return [p for p in self.points if p in rect]
        return (self.NE._search(rect) +
                self.NW._search(rect) +
                self.SW._search(rect) +
                self.SE._search(rect))


class QuadTree:
    def __init__(self, points: list[Point]):
        self._root = Node(Rectangle.boundary(points), points)
        self._create()

    def search(self, rect: Rectangle) -> list[Point]:
        return self._root._search(rect)

    def _create(self):
        self._root._divide_recursively()

    def __str__(self):
        return self._root.stringify()


