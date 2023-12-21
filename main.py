from visualizer import Visualizer, pg
from kdtree import KDTree


def main():
    vis = Visualizer(flags=pg.RESIZABLE)
    visualization = False
    vis.set_scene_delay(10)
    KDTree(visualizer=vis, show_visualization=visualization)
    vis.run()


if __name__ == '__main__':
    main()
