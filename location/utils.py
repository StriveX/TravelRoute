from .models import *
from math import hypot

def calc_distance(pointA, pointB):
    return hypot(pointA[0] - pointB[0], pointA[1] - pointB[1])


def insert_into_geo_tree(point, geo_tree_root, level):
    level -= 1
    if level == 0:
        geo_tree_root.children.append(point)
        geo_tree_root.num_children += 1
    else:
        if geo_tree_root.num_children == 0:
            new_cluster = Cluster(center_latlng=point, level=level, num_children=0)
            geo_tree_root.locations.append(new_cluster)
            geo_tree_root.num_children += 1
            insert_into_geo_tree(point, new_cluster, level)
        else:
            min_dist = float('Inf')
            nearest_child = None
            for child_tree in geo_tree_root.children:
                local_dist = calc_distance(child_tree.center_latlng, point)
                if local_dist < min_dist and local_dist < ZOOM_LEVEL[level]:
                    min_dist = local_dist
                    nearest_child = child_tree
            if nearest_child:
                insert_into_geo_tree(point, nearest_child, level)
            else:
                new_cluster = Cluster(center_latlng=point, level=level, num_children=0)
                geo_tree_root.locations.append(new_cluster)
                geo_tree_root.num_children += 1
                insert_into_geo_tree(point, new_cluster, level)


def calculate_route(points):
    geo_tree = Cluster()
    for point in points:
        insert_into_geo_tree(point, geo_tree, 6)
    return geo_tree


def calculate_route_wrapper(places):
    points = [place for place in places]
    geo_tree = calculate_route(points)
    return geo_tree


def find_mst_prim(points):
    """
    @ param: points' first point is the begin point
    """
    length = len(points)
    parent = [0] * length
    key = [0] * length


def find_shortest_path(points):
    find_mst_prim()


def find_shortest_path_wrapper(geo_tree, begin):
