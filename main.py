from visualizer import Visualizer, pg, Point
from Assets.tests import Test, Rectangle, TestCollection, PointsCollection, RectsCollection, Color
from kdtree import KDTree
from sys import setrecursionlimit
from comparison import *
import timer as t

setrecursionlimit(1000000000)


def main():

    print(t.uniform_times, t.border_times, t.edge_times, t.qt_uniform_times, t.qt_bound_times, t.qt_cluster_times, sep='\n')


if __name__ == '__main__':
    main()
