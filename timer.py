import timeit
import kdtree as kt
import comparison as cmp
import visualizer as vs
import quadtree


uniform_times = []
uniform_point_results = []
region = vs.Rectangle(-1, -1, 1001, 1001)
search_region = vs.Rectangle(*cmp.UNIFORM_REGION)
for u in cmp.UNIFORM:
    tree = kt.KDTree(points=vs.PointsCollection(list(map(lambda p: vs.Point(*p, 1), u))),
                     region=vs.Rectangle(*cmp.UNIFORM_REGION), show_visualization=False)
    tree.build()
    points = [point for point in tree.points if point in tree.region]
    start = timeit.default_timer()
    result = tree.search()
    end = timeit.default_timer()
    uniform_point_results.append((points, result))
    uniform_times.append((len(tree.points), len(result), end - start))

border_times = []
border_point_results = []
for b in cmp.BOUND:
    tree = kt.KDTree(points=vs.PointsCollection(list(map(lambda p: vs.Point(p[0], p[1], 1), b))),
                     region=vs.Rectangle(*cmp.BOUND_REGION), show_visualization=False)
    tree.build()
    points = [point for point in tree.points if point in tree.region]
    start = timeit.default_timer()
    result = tree.search()
    end = timeit.default_timer()
    border_point_results.append((points, result))
    border_times.append((len(tree.points), len(result), end - start))

edge_times = []
edge_point_results = []
for e in cmp.EDGE:
    tree = kt.KDTree(points=vs.PointsCollection(list(map(lambda p: vs.Point(p[0], p[1], 1), e))),
                     region=vs.Rectangle(*cmp.EDGE_REGION), show_visualization=False)
    tree.build()
    points = [point for point in tree.points if point in tree.region]
    start = timeit.default_timer()
    result = tree.search()
    end = timeit.default_timer()
    edge_point_results.append((points, result))
    edge_times.append((len(tree.points), len(result), end - start))


qt_uniform_times = []
uniform_rect = quadtree.Rectangle.from_tuples(
        (cmp.UNIFORM_REGION[0], cmp.UNIFORM_REGION[0] + cmp.UNIFORM_REGION[2]),
        (cmp.UNIFORM_REGION[1], cmp.UNIFORM_REGION[1] + cmp.UNIFORM_REGION[3])
    )
for u in cmp.UNIFORM:
    qt = quadtree.QuadTree(u)
    start = timeit.default_timer()
    result = qt.search(uniform_rect)
    end = timeit.default_timer()
    qt_uniform_times.append((len(u), len(result), end - start))

qt_bound_times = []
bound_rect = quadtree.Rectangle.from_tuples(
        (cmp.BOUND_REGION[0], cmp.BOUND_REGION[0] + cmp.BOUND_REGION[2]),
        (cmp.BOUND_REGION[1], cmp.BOUND_REGION[1] + cmp.BOUND_REGION[3])
    )

for u in cmp.BOUND:
    qt = quadtree.QuadTree(u)
    start = timeit.default_timer()
    result = qt.search(bound_rect)
    end = timeit.default_timer()
    qt_bound_times.append((len(u), len(result), end - start))

qt_cluster_times = []
cluster_rect = quadtree.Rectangle.from_tuples(
        (cmp.EDGE_REGION[0], cmp.EDGE_REGION[0] + cmp.EDGE_REGION[2]),
        (cmp.EDGE_REGION[1], cmp.EDGE_REGION[1] + cmp.EDGE_REGION[3])
    )

for u in cmp.EDGE:
    qt = quadtree.QuadTree(u)
    start = timeit.default_timer()
    result = qt.search(cluster_rect)
    end = timeit.default_timer()
    qt_cluster_times.append((len(u), len(result), end - start))
