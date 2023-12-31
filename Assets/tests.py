from visualizer import Point, Rectangle, PointsCollection, pg, RectsCollection, Color
from Assets.shapesCollections import Collection
from timeit import default_timer
from kdtree import KDTree, Visualizer


class Test:
    def __init__(self, points: PointsCollection, region: Rectangle, message: str = ''):
        self.points = points
        self.region = region
        self.message = message

    def __str__(self):
        return f'{len(self.points), self.message}'


class TestCollection(Collection):
    def __init__(self, items: list[Test], tree: KDTree = None, copy: bool = False):
        super(TestCollection, self).__init__(items, None, copy)
        self.__tree = tree

    def runtests(self):
        if self.__tree is None: return
        for test in self.items:
            self.__tree.set_parameters(test.points, test.region)
            start = default_timer()
            self.__tree.build()
            end = default_timer()
            kdtree_build_time = end - start
            start = default_timer()
            result = self.__tree.search()
            end = default_timer()
            search_time = end - start
            start = default_timer()
            brute_result = self.__tree.brute_force
            end = default_timer()
            brute_force_time = end - start
            print(f'{test.message}\nKD-Tree build time:\n{kdtree_build_time}s\n\nSearch time: \n{search_time}s\n\nBrute Force:'
                  f'\n{brute_force_time}s\n\n'
                  f'{set(result).difference(set(brute_result))}\n\n'
                  f'{len(result), len(brute_result)}\n\n')
