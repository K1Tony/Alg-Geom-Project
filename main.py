from visualizer import Visualizer, pg
from Assets.tests import Test, Rectangle, TestCollection, PointsCollection, RectsCollection, Color
from kdtree import KDTree
from sys import setrecursionlimit

setrecursionlimit(1000000000)


def main():
    vis = Visualizer(flags=pg.RESIZABLE)
    vis.set_scene_delay(50)
    vis.set_point_radius(100)
    randoms = TestCollection([Test(vis.generate_random_points(point_count=100 * (i + 1)),
                                   Rectangle(vis.control_panel_width,
                                             vis.control_panel_width + vis.control_panel_width,
                                             vis.width // 3, vis.height // 2,
                                             fill_color=Color.GREEN, border_width=0, alpha=50))
                              for i in range(5)])
    tree = KDTree(visualizer=vis)
    vis.run()


if __name__ == '__main__':
    main()
