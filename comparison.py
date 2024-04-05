from numpy.random import uniform


def create_uniform(bound_x, bound_y, point_count=100):
    UNIFORM = [(uniform(*bound_x), uniform(*bound_y)) for _ in range(point_count)]
    return UNIFORM


def create_bounds_points(bound_x, bound_y, point_count=100):
    left = [(bound_x[0], uniform(*bound_y)) for _ in range(point_count // 4)]
    right = [(bound_x[1], uniform(*bound_y)) for _ in range(point_count // 4)]
    top = [(uniform(*bound_x), bound_y[0]) for _ in range(point_count // 4)]
    bot = [(uniform(*bound_x), bound_y[1]) for _ in range(point_count // 4)]

    return top + left + right + bot


def create_edge_cluster(max_x, max_y, bound_x, bound_y, point_count=100):
    edges = [(bound_x[0], max_y), (max_x, max_y), (max_x, bound_y[0])]
    points = [(uniform(*bound_x), uniform(*bound_y)) for _ in range(point_count)]
    return points + edges


UNIFORM = [create_uniform((0, 1000), (0, 1000), 1000 * (i + 1)) for i in range(10)]
UNIFORM_REGION = 200, 200, 500, 500
BOUND = [create_bounds_points((5, 1000), (5, 1000), 500 * (i + 1)) for i in range(10)]
BOUND_REGION = 0, 0, 800, 800
EDGE = [create_edge_cluster(1000, 1000, (0, 10), (0, 10), 10 * i) for i in range(5)]
EDGE_REGION = 0, 0, 100, 100
