from visualizer import Visualizer, pg, Color, Rectangle, RectsCollection, PointsCollection
from kdtree import KDTree


def main():
    vis = Visualizer(flags=pg.RESIZABLE)
    vis.set_scene_delay(100)
    tree = KDTree(visualizer=vis)
    vis.run()


if __name__ == '__main__':
    main()
