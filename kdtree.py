from visualizer import Visualizer, Color, Point, Line, PointsCollection, LinesCollection, Rectangle, RectsCollection


def partition(T, p, q, key):
    if p >= q: return
    i = p - 1
    pivot = key(T[q])
    for j in range(p, q):
        if key(T[j]) < pivot:
            i += 1
            T[i], T[j] = T[j], T[i]
    i += 1
    T[i], T[q] = T[q], T[i]
    return i


def quick_select(T, p, q, k, key):
    if p >= q: return T[k]
    i = partition(T, p, q, key)
    if i == k: return T[i]
    if i < k: return quick_select(T, i + 1, q, k, key)
    return quick_select(T, p, i - 1, k, key)


def median(T, key):
    return quick_select(T, 0, len(T) - 1, len(T) // 2, key)


class _KDTreeNode:
    def __init__(self, points, line=None, region=None, left=None, right=None, parent=None):
        self.__points = points
        self.__line = line
        self.__region = region
        self.__left = left
        self.__right = right
        self.__parent = parent

    @property
    def points(self):
        return self.__points

    @property
    def line(self):
        return self.__line

    @property
    def region(self):
        return self.__region

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    @property
    def parent(self):
        return self.__parent

    def is_leaf(self):
        return self is not None and self.left is None and self.right is None

    def is_left_child(self):
        if self is None or self.parent is None: return False
        return self.parent.left is self

    def is_right_child(self):
        if self is None or self.parent is None: return False
        return self.parent.right is self


class KDTree:
    __MAX_WIDTH = 6

    def __init__(self, points: PointsCollection = PointsCollection(), region: Rectangle | None = None,
                 visualizer: Visualizer | None = None):
        self.__points = points
        self.__visualizer = visualizer
        self.__region = region if region is not None else Rectangle()
        self.__root = None

        self.__state = 0

        self.__play_button_index = self.__visualizer.BUTTON_COUNT

        self.__button_key = "KDTREE"

        self.__visualizer.add_button("Build KD-Tree", self.__button_key, self.build)
        self.__visualizer.add_repeatable(self.__get_data_from_visualizer)

    def __get_data_from_visualizer(self):
        self.__points = self.__visualizer.points
        self.__region = self.__visualizer.search_region

    def __intersects(self, item: Rectangle):
        return item.colliderect(self.region)

    def __build(self, points, depth=0, visualization=True, upper_end=None, lower_end=None, left_end=None, right_end=None):
        if upper_end is None: upper_end = 0
        if left_end is None: left_end = self.__visualizer.control_panel_width
        if right_end is None: right_end = self.__visualizer.width
        if lower_end is None: lower_end = self.__visualizer.height
        region = Rectangle(upper_end, left_end, right_end - left_end, lower_end - upper_end, fill_color=Color.BLUE,
                           alpha=100)
        if len(points) < 1 or not self.__intersects(region):
            return []
        if region in self.region:
            region.color = Color.PURPLE
            if visualization:
                copied_points = PointsCollection(list(map(lambda point: point.__copy__(), points)), color=Color.BLACK)
                self.__visualizer.add_scene(
                    points=self.__visualizer.last_scene.points + copied_points,
                    lines=self.__visualizer.last_scene.lines,
                    rects=RectsCollection([self.region, region])
                )
            return points
        if len(points) == 1:
            if points[0] in self.region:
                if visualization:
                    copied_points = PointsCollection(list(map(lambda point: point.__copy__(), points)),
                                                     color=Color.BLACK)
                    self.__visualizer.add_scene(
                        points=self.__visualizer.last_scene.points + copied_points,
                        lines=self.__visualizer.last_scene.lines,
                        rects=RectsCollection([self.region, region])
                    )
                return points
            return []
        width = 2 if self.__MAX_WIDTH - depth < 2 else self.__MAX_WIDTH - depth
        result = []
        if depth % 2 == 1:
            pt = median(points, key=lambda point: point.y)
            i = points.index(pt)
            LT = points[:i]
            RT = points[i:]
            line = Line(Point(left_end, pt.y, self.__visualizer.point_radius),
                        Point(right_end, pt.y, self.__visualizer.point_radius), color=Color.BLUE, width=width)
            regions = RectsCollection([Rectangle(upper_end, left_end, right_end - left_end, pt.y - upper_end,
                                                 fill_color=Color.GREEN, alpha=50),
                                       Rectangle(pt.y, left_end, right_end - left_end, lower_end - pt.y,
                                                 fill_color=Color.RED, alpha=50)])
            if visualization:
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))
            if pt in self.region:
                result.append(pt)
                if visualization:
                    self.__visualizer.update_last_scene(points=self.__visualizer.last_scene.points +
                                                        PointsCollection([pt.__copy__()], color=Color.BLACK))
            result += self.__build(LT, depth + 1, visualization, upper_end=upper_end, lower_end=pt.y, left_end=left_end,
                                right_end=right_end)
            result += self.__build(RT, depth + 1, visualization, upper_end=pt.y, lower_end=lower_end, left_end=left_end,
                                 right_end=right_end)
        else:
            pt = median(points, key=lambda point: point.x)
            i = points.index(pt)
            LT = points[:i]
            RT = points[i:]
            line = Line(Point(pt.x, upper_end, self.__visualizer.point_radius),
                        Point(pt.x, lower_end, self.__visualizer.point_radius), color=Color.BLUE, width=width)
            regions = RectsCollection([Rectangle(upper_end, left_end, pt.x - left_end, lower_end - upper_end,
                                                 fill_color=Color.GREEN, alpha=50),
                                       Rectangle(upper_end, pt.x, right_end - pt.x, lower_end - upper_end,
                                                 fill_color=Color.RED, alpha=50)])
            if visualization:
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))
            if pt in self.region:
                result.append(pt)
                if visualization:
                    self.__visualizer.update_last_scene(points=self.__visualizer.last_scene.points +
                                                        PointsCollection([pt.__copy__()], color=Color.BLACK))
            result += self.__build(LT, depth + 1, visualization, upper_end=upper_end, lower_end=lower_end, right_end=pt.x,
                                left_end=left_end)
            result += self.__build(RT, depth + 1, visualization, upper_end=upper_end, lower_end=lower_end, left_end=pt.x,
                                 right_end=right_end)
        return result

    @property
    def visualizer(self):
        return self.__visualizer

    @property
    def points(self):
        return self.__points

    @property
    def region(self):
        return self.__region

    def build(self, visualization=True):
        self.__visualizer.add_scene(points=self.points,
                                    lines=self.__visualizer.lines,
                                    rects=RectsCollection([self.region]))
        result = self.__build(self.__points, visualization=visualization)
        return result
