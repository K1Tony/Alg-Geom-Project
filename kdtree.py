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
    def __init__(self, point, line=None, region=None, left=None, right=None, parent=None):
        self.__point = point
        self.__line = line
        self.__region = region
        self.__left = left
        self.__right = right
        self.__parent = parent

    @property
    def point(self):
        return self.__point

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
        self.__points = points.items
        self.__visualizer = visualizer
        self.__region = region if region is not None else Rectangle()
        self.__root = None

        self.__state = 0

        self.__visualizer.add_button(self.__message, self.__onclick)
        self.__visualizer.add_button("Save changes", self.__get_data_from_visualizer)

    def __contains__(self, item: Point | Rectangle):
        if isinstance(item, Point):
            return self.region.x <= item.x <= self.region.x + self.region.w and\
                   self.region.y <= item.y <= self.region.y + self.region.h
        if isinstance(item, Rectangle):
            return self.region.x <= item.x and self.region.y <= item.y and\
                   self.region.w >= item.w and self.region.h >= item.h
        return False

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
        if len(points) < 1:
            return None
        if len(points) == 1:
            region.color = Color.PURPLE
            return _KDTreeNode(points[0], region=region, left=None, right=None)
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
            if visualization:
                self.__visualizer.add_updated_scene(lines=LinesCollection([line]))
                self.__visualizer.update_last_scene(rects=regions + RectsCollection([self.region]))
            left = self.__build(LT, depth + 1, visualization, upper_end=upper_end, lower_end=pt.y, left_end=left_end,
                                right_end=right_end)
            right = self.__build(RT, depth + 1, visualization, upper_end=pt.y, lower_end=lower_end, left_end=left_end,
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
            left = self.__build(LT, depth + 1, visualization, upper_end=upper_end, lower_end=lower_end, right_end=pt.x,
                                left_end=left_end)
            right = self.__build(RT, depth + 1, visualization, upper_end=upper_end, lower_end=lower_end, left_end=pt.x,
                                 right_end=right_end)

        return _KDTreeNode(pt, line, region, left, right)

    def __get_leaves(self, node: _KDTreeNode, leaves):
        if node is None:
            return
        if node.is_leaf():
            leaves.append(node)
            return
        self.__get_leaves(node.left, leaves)
        self.__get_leaves(node.right, leaves)

    def __search(self, node: _KDTreeNode, result, result_color: tuple[int, int, int] = Color.BLACK, visualization: bool = True):
        if node is None:
            return
        if visualization:
            self.__visualizer.add_scene(self.__visualizer.last_scene.points,
                                        self.__visualizer.last_scene.lines,
                                        RectsCollection([node.region, self.region]))
        if node.is_leaf() and node.point in self.region:
            node.point.color = result_color
            if visualization:
                self.__visualizer.update_last_scene(rects=RectsCollection([node.region], color=Color.PURPLE) +
                                                    RectsCollection([self.region], color=Color.GREEN))
            result.append(node.point)
            return
        if node.left is not None:
            if self.__intersects(node.left.region):
                self.__search(node.left, visualization=visualization, result=result)
        if node.right is not None:
            if self.__intersects(node.right.region):
                self.__search(node.right, visualization=visualization, result=result)

    def __collapse(self):
        self.__visualizer.clear_scenes()

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
    def __message(self):
        return "Create KD-Tree" if self.__state == 0 else "Search KD-Tree" if self.__state == 1 else "Collapse KD-Tree"

    @property
    def __onclick(self):
        return self.build if self.__state == 0 else self.search if self.__state == 1 else self.collapse

    def build(self, visualization=True):
        self.__visualizer.add_scene(points=self.points, rects=RectsCollection([self.region]))
        self.__root = self.__build(self.__points, visualization=visualization)
        self.__state = 1
        self.visualizer.update_button(3, self.__message, self.__onclick)

    def search(self, visualization=True):
        result = []
        self.__search(self.__root, visualization=visualization, result=result)
        self.__state = 2
        self.visualizer.update_button(3, self.__message, self.__onclick)
        return result

    def collapse(self):
        self.__collapse()
        self.__state = 0
        self.visualizer.update_button(3, self.__message, self.__onclick)
