from visualizer import Visualizer, Point, PointsCollection, RectsCollection, Rectangle, Color
from kdtree import KDTree
from sys import setrecursionlimit
from random import uniform
from comparison import *

setrecursionlimit(1000000000)


def main():
    vis = Visualizer()
    vis.set_point_radius(100)
    vis.set_scene_delay(50)
    POINTS, REGION = PointsCollection(), Rectangle()
    POINTS_BOUND, REGION_BOUND = PointsCollection(list(map(lambda p: Point(*p, vis.point_radius),
                                                           create_bounds_points((vis.control_panel_width, vis.width),
                                                                                (0, vis.height), 500)))), Rectangle(0, vis.control_panel_width,
                                                                                                                    vis.width // 2, vis.height // 2,
                                                                                                                    fill_color=Color.GREEN, alpha=50)
    POINTS_CLUSTER, REGION_CLUSTER = PointsCollection(list(map(lambda p: Point(*p, vis.point_radius),
                                                               create_edge_cluster(vis.width - vis.point_radius,
                                                                                   vis.height - vis.point_radius,
                                                                                   (vis.control_panel_width, vis.control_panel_width + 10),
                                                                                   (0, 10), 53)))), Rectangle(0, vis.control_panel_width,
                                                                                                              100, 100, fill_color=Color.GREEN,
                                                                                                              alpha=50)
    POINTS_CROSS, REGION_CROSS = PointsCollection([Point(uniform(vis.control_panel_width, vis.width), vis.height // 2, vis.point_radius) for _ in range(200)] +
                                                  [Point(vis.width // 2, uniform(0, vis.height), vis.point_radius) for _ in range(200)]),\
    Rectangle(vis.height // 4, (vis.width - vis.control_panel_width) // 4,(vis.width - vis.control_panel_width) // 2, vis.height // 2,
              fill_color=Color.GREEN, alpha=50)

    # example point structures to visualize

    #POINTS, REGION = POINTS_BOUND, REGION_BOUND
    #POINTS, REGION = POINTS_CLUSTER, REGION_CLUSTER
    POINTS, REGION = POINTS_CROSS, REGION_CROSS
    kt = KDTree(visualizer=vis, points=POINTS, region=REGION)
    vis.run()


if __name__ == '__main__':
    main()
