from visualizer import Visualizer, pg
from kdtree import KDTree


def main():
    vis = Visualizer(flags=pg.RESIZABLE)
    vis.set_scene_delay(10)
    KDTree(visualizer=vis)
    vis.run()


if __name__ == '__main__':
    main()
