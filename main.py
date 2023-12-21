from visualizer import Visualizer, pg, LinesCollection, Color, Rectangle, RectsCollection, PointsCollection, Point
from kdtree import KDTree


def main():
    vis = Visualizer(flags=pg.RESIZABLE)
    vis.set_scene_delay(100)
    tree = KDTree(visualizer=vis)
    vis.run()


if __name__ == '__main__':
    main()
