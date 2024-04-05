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
    def __init__(self, points, region=None, left=None, right=None, parent=None):
        self.__points = points
        self.__region = region
        self.__left = left
        self.__right = right

    @property
    def points(self):
        return self.__points

    @property
    def region(self):
        return self.__region

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    def is_leaf(self):
        return self is not None and self.left is None and self.right is None


class KDTree:
    __MAX_WIDTH = 6

    def __init__(self, points: PointsCollection = PointsCollection(), region: Rectangle | None = None,
                 visualizer: Visualizer | None = None, show_visualization: bool = True):
        self.__points = points
        self.__visualizer = visualizer
        self.__region = region
        self.__root = None

        self.__show_visualization = show_visualization

        if self.__show_visualization:
            self.__button_key = "KDTREE"
            self.__search_key = "SEARCH"
            self.__visualizer.add_button("Build KD-Tree", self.__button_key, self.build)
            self.__visualizer.add_button("Search KD-Tree", self.__search_key, self.search)
            self.__visualizer.add_repeatable(self.__get_data_from_visualizer)
            if len(self.points) > 0: self.__visualizer.add_points(self.__points)
            if self.region is not None: self.__visualizer.search_region = region

    def __get_data_from_visualizer(self):
        self.__points = self.__visualizer.points
        self.__region = self.__visualizer.search_region

    def __build(self, points, depth=0, upper_end=None, lower_end=None, left_end=None, right_end=None):
        if len(points) < 1:
            return None
        if upper_end is None: upper_end = min(points, key=lambda point: point.y).y - points[0].radius
        if left_end is None: left_end = min(points).x - points[0].radius
        if right_end is None: right_end = max(points).x + points[0].radius
        if lower_end is None: lower_end = max(points, key=lambda point: point.y).y + points[0].radius
        region = Rectangle(upper_end, left_end,
                           right_end - left_end,
                           lower_end - upper_end, fill_color=Color.BLUE,
                           alpha=100)
        if len(points) == 1:
            return _KDTreeNode(points, region=region)
        width = 2 if self.__MAX_WIDTH - depth < 2 else self.__MAX_WIDTH - depth
        if depth % 2 == 1:
            pt = median(points, key=lambda point: point.y)
            i = points.index(pt)
            LT = points[:i]
            RT = points[i:]
            if self.__show_visualization:
                line = Line(Point(left_end, pt.y, 1),
                            Point(right_end, pt.y, 1), color=Color.BLUE, width=width)
                regions = RectsCollection([Rectangle(upper_end, left_end, right_end - left_end, pt.y - upper_end,
                                                     fill_color=Color.GREEN, alpha=50),
                                           Rectangle(pt.y, left_end, right_end - left_end, lower_end - pt.y,
                                                     fill_color=Color.RED, alpha=50)])
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))
            left = self.__build(LT, depth + 1, upper_end=upper_end, lower_end=pt.y,
                                left_end=left_end, right_end=right_end)
            right = self.__build(RT, depth + 1, upper_end=pt.y, lower_end=lower_end,
                                 left_end=left_end, right_end=right_end)
        else:
            pt = median(points, key=lambda point: point.x)
            i = points.index(pt)
            LT = points[:i]
            RT = points[i:]
            if self.__show_visualization:
                line = Line(Point(pt.x, upper_end, 1),
                            Point(pt.x, lower_end, 1), color=Color.BLUE, width=width)
                regions = RectsCollection([Rectangle(upper_end, left_end, pt.x - left_end, lower_end - upper_end,
                                                     fill_color=Color.GREEN, alpha=50),
                                           Rectangle(upper_end, pt.x, right_end - pt.x, lower_end - upper_end,
                                                     fill_color=Color.RED, alpha=50)])
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))

            left = self.__build(LT, depth + 1, upper_end=upper_end, lower_end=lower_end,
                                right_end=pt.x, left_end=left_end)
            right = self.__build(RT, depth + 1, upper_end=upper_end, lower_end=lower_end,
                                 right_end=right_end, left_end=pt.x)
        return _KDTreeNode(points, region, left, right)

    def __search(self, node: _KDTreeNode, result: list[Point]):
        if node is None or not self.region.colliderect(node.region):
            return
        if node.is_leaf():
            if node.points[0] in self.region:
                result += node.points
                if self.__show_visualization:
                    self.__visualizer.add_scene(points=self.__visualizer.points +
                                                PointsCollection(result, color=Color.BLACK, copy=True),
                                                lines=self.__visualizer.lines,
                                                rects=RectsCollection([self.region]) +
                                                RectsCollection([node.region.__copy__()], color=Color.PURPLE))
                return
            if self.__show_visualization:
                self.__visualizer.add_scene(points=self.__visualizer.points +
                                            PointsCollection(result, color=Color.BLACK, copy=True),
                                            lines=self.__visualizer.lines,
                                            rects=RectsCollection([self.region, node.region]))
            return
        if node.region in self.region:
            result += node.points
            if self.__show_visualization:
                self.__visualizer.add_scene(points=self.__visualizer.points +
                                            PointsCollection(result, color=Color.BLACK, copy=True),
                                            lines=self.__visualizer.lines,
                                            rects=RectsCollection([self.region]) +
                                            RectsCollection([node.region.__copy__()], color=Color.PURPLE))
            return
        if self.region.colliderect(node.region):
            if self.__show_visualization:
                self.__visualizer.add_scene(points=self.__visualizer.points +
                                            PointsCollection(result, color=Color.BLACK, copy=True),
                                            lines=self.__visualizer.lines,
                                            rects=RectsCollection([self.region, node.region]))
            self.__search(node.left, result)
            self.__search(node.right, result)

    @property
    def visualizer(self):
        return self.__visualizer

    @property
    def points(self):
        return self.__points

    @property
    def region(self):
        return self.__region

    def build(self):
        if self.__show_visualization:
            self.__visualizer.clear_scenes()
            self.__visualizer.add_scene(points=self.points,
                                        lines=self.__visualizer.lines,
                                        rects=RectsCollection([self.region]))
        self.__root = self.__build(self.__points.items)
        if self.__show_visualization:
            self.__visualizer.add_scene(points=self.points,
                                    lines=self.__visualizer.last_scene.lines,
                                    rects=RectsCollection([self.region]))

    def search(self):
        result = []
        if self.__show_visualization:
            first_scene = self.__visualizer.first_scene
            self.__visualizer.clear_scenes()
            self.__visualizer.add_scene(first_scene.points, first_scene.lines, first_scene.rects)
        self.__search(self.__root, result)
        if self.__show_visualization:
            self.__visualizer.add_scene(points=self.visualizer.last_scene.points,
                                        lines=self.visualizer.last_scene.lines,
                                        rects=RectsCollection([self.region]))
        return result

    def set_parameters(self, points=None, region=None):
        if points is not None: self.__points = points
        if region is not None: self.__region = region
