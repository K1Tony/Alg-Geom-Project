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
        self.__parent = parent

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
                 visualizer: Visualizer | None = Visualizer(), show_visualization: bool = True):
        self.__points = points
        self.__visualizer = visualizer
        self.__region = region if region is not None else Rectangle()
        self.__root = None

        self.__show_visualization = show_visualization

        self.__state = 0

        self.__button_key = "KDTREE"
        self.__search_key = "SEARCH"

        self.__visualizer.add_button("Build KD-Tree", self.__button_key, self.build)
        self.__visualizer.add_button("Search KD-Tree", self.__search_key, self.search)
        self.__visualizer.add_repeatable(self.__get_data_from_visualizer)

    def __get_data_from_visualizer(self):
        self.__points = self.__visualizer.points
        self.__region = self.__visualizer.search_region

    def __intersects(self, item: Rectangle):
        return item.colliderect(self.region)

    def __build(self, points, lines, depth=0, upper_end=None, lower_end=None, left_end=None, right_end=None):
        if upper_end is None: upper_end = 0
        if left_end is None: left_end = self.__visualizer.control_panel_width
        if right_end is None: right_end = self.__visualizer.width
        if lower_end is None: lower_end = self.__visualizer.height
        region = Rectangle(upper_end, left_end,
                           right_end - left_end,
                           lower_end - upper_end, fill_color=Color.BLUE,
                           alpha=100)
        if len(points) < 1:
            return None
        if len(points) == 1:
            return _KDTreeNode(points, region=region)
        width = 2 if self.__MAX_WIDTH - depth < 2 else self.__MAX_WIDTH - depth
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
            if self.__show_visualization:
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))
            left = self.__build(LT, lines, depth + 1, upper_end=upper_end, lower_end=pt.y, left_end=left_end,
                                right_end=right_end)
            right = self.__build(RT, lines, depth + 1, upper_end=pt.y, lower_end=lower_end, left_end=left_end,
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
            if self.__show_visualization:
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))
            left = self.__build(LT, lines, depth + 1, upper_end=upper_end, lower_end=lower_end, right_end=pt.x,
                                left_end=left_end)
            right = self.__build(RT, lines, depth + 1, upper_end=upper_end, lower_end=lower_end, left_end=pt.x,
                                 right_end=right_end)
        lines.append(line)
        return _KDTreeNode(points, region, left, right)

    def __build_tree(self, points, depth=0):
        if len(points) < 1:
            return None
        if len(points) == 1:
            return _KDTreeNode(...)
        if depth % 2 == 0:
            pt = median(points, key=lambda point: point.x)
        else:
            pt = median(points, key=lambda point: point.y)
        i = points.index(pt)
        LT, RT = points[:i], points[i:]
        left_node = self.__build_tree(LT, depth + 1)
        right_node = self.__build_tree(RT, depth + 1)
        return _KDTreeNode(..., left=left_node, right=right_node)

    def __search_tree(self, node: _KDTreeNode):

        if node.is_leaf() or node.region in self.region:

            return node.points

        result = []

        if self.region.colliderect(node.region):

            result += self.__search_tree(node.left)
            result += self.__search_tree(node.right)

        return result

    def __search(self, node: _KDTreeNode, search_region: Rectangle, result: list[Point]):
        if node is None:
            return
        if node.is_leaf():
            if node.points[0] in search_region:
                result += node.points
                if self.__show_visualization:
                    self.__visualizer.add_scene(points=self.__visualizer.points +
                                                PointsCollection(result, color=Color.BLACK, copy=True),
                                                lines=self.__visualizer.lines,
                                                rects=RectsCollection([search_region]) +
                                                RectsCollection([node.region.__copy__()], color=Color.PURPLE))
            if self.__show_visualization:
                self.__visualizer.add_scene(points=self.__visualizer.points +
                                            PointsCollection(result, color=Color.BLACK, copy=True),
                                            lines=self.__visualizer.lines,
                                            rects=RectsCollection([search_region, node.region]))
            return
        if node.region in search_region:
            result += node.points
            if self.__show_visualization:
                self.__visualizer.add_scene(points=self.__visualizer.points +
                                            PointsCollection(result, color=Color.BLACK, copy=True),
                                            lines=self.__visualizer.lines,
                                            rects=RectsCollection([search_region]) +
                                            RectsCollection([node.region.__copy__()], color=Color.PURPLE))
            return
        if search_region.colliderect(node.region):
            if self.__show_visualization:
                self.__visualizer.add_scene(points=self.__visualizer.points +
                                            PointsCollection(result, color=Color.BLACK, copy=True),
                                            lines=self.__visualizer.lines,
                                            rects=RectsCollection([search_region, node.region]))
            self.__search(node.left, search_region, result)
            self.__search(node.right, search_region, result)

    @property
    def visualizer(self):
        return self.__visualizer

    @property
    def points(self):
        return self.__points

    @property
    def region(self):
        return self.__region

    @property
    def brute_force(self):
        return [point for point in self.points if point in self.region]

    def build(self):
        if self.__show_visualization:
            self.__visualizer.clear_scenes()
            self.__visualizer.add_scene(points=self.points,
                                        lines=self.__visualizer.lines,
                                        rects=RectsCollection([self.region]))
        lines = []
        self.__root = self.__build(self.__points.items, lines)
        return LinesCollection(lines)

    def search(self):
        result = []
        if self.__show_visualization:
            first_scene = self.__visualizer.first_scene
            self.__visualizer.clear_scenes()
            self.__visualizer.add_scene(first_scene.points, first_scene.lines, first_scene.rects)
        self.__search(self.__root, self.region, result)
        if self.__show_visualization:
            self.__visualizer.add_scene(points=self.visualizer.last_scene.points,
                                        lines=self.visualizer.last_scene.lines,
                                        rects=RectsCollection([self.region]))
        return result

    def set_parameters(self, points=None, region=None):
        if points is not None: self.__points = points
        if region is not None: self.__region = region

