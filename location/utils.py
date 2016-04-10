from .models import *
from math import hypot


class DictMinHeap:
    def __init__(self, elements):
        self.size = len(elements)
        self.elements = elements

    def bubble_up(self, i, K):
        while (i-1)/2 >= 0:
            if self.elements[(i-1)/2] > self.elements[i]:
                tmp = self.elements[i]
                self.elements[i] = self.elements[(i-1)/2]
                self.elements[(i-1)/2] = tmp
            i = (i-1)/2

    def bubble_down(self, i, K):
        while i * 2 < self.size:
            left = K[self.elements[2*i+1]]
            right = K[self.elements[2*i+2]]
            small_child_index = 2*i+1 if left < right else 2*i+2
            if K[self.elements[i]] > K[self.elements[small_child_index]]:
                tmp = self.elements[i]
                self.elements[i] = self.elements[small_child_index]
                self.elements[small_child_index] = tmp
                i = small_child_index
            else:
                break

    def heapify(self, K):
        n = len(self.elements) - 1
        for i in range(n/2):
            self.bubble_down(i, K)

    def del_min(self, K):
        min_val = self.elements[0]
        self.elements[0] = self.elements[self.size-1]
        self.bubble_down(0, K)
        self.size -= 1
        del self.elements[self.size]
        return min_val


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


def build_geo_tree(points):
    geo_tree = Cluster(center_latlng=points[0], level=6, num_children=0)
    insert_into_geo_tree(points[0], geo_tree, 6)
    for point in points[1:]:
        insert_into_geo_tree(point, geo_tree, 6)
    return geo_tree


def find_mst_prim(points):
    """
        :param points first point is the begin point
    """
    length = len(points)
    P = [-1] * length
    mst = {}
    Q = []
    for i in range(len(points)):
        mst[i] = []
        Q.append(i)
    pq = DictMinHeap(Q)
    unlinked_points = list(Q)
    K = [float('Inf')] * length
    K[0] = 0  # begin point

    while len(unlinked_points) > 0:
        u = pq.del_min(K)
        unlinked_points.remove(u)
        mst[P[u]].append(u)

        for v in unlinked_points:
            w = calc_distance(points[u], points[v])
            if len(unlinked_points) > 0 and w < K[v]:
                P[v] = u
                K[v] = w
        pq.heapify(K)
    return mst


def approximate_tsp_by_mst(index, mst, points, result):
    """
    Depth search first,
    see http://www.geeksforgeeks.org/travelling-salesman-problem-set-2-approximate-using-mst/
    :param index:
    :param mst: minimum spanning tree of index
    :param points: original points
    :param result: list of Point
    :return: None
    """
    if len(mst[index]) == 0:
        result.append(points[index])
    else:
        for child in mst[index]:
            approximate_tsp_by_mst(child, mst, points, result)
        result.append(points[index])


def find_shortest_path(points):
    """

    :param points: a random list of Point
    :return: a list of Point joined by approximate shortest path
    """
    mst = find_mst_prim(points)
    result = []
    approximate_tsp_by_mst(0, mst, points, result)
    return result


def find_shortest_path_wrapper(geo_tree):
    if geo_tree.level == 1:
        return
    children = geo_tree.children
    path = find_shortest_path(children)
    geo_tree.path = path
    for i, sorted_child in enumerate(path):
        local_child_child = sorted_child.children
        if i < len(path) - 1:
            next_sorted_child = path[i+1]
            min_dist = float('Inf')
            nearest_child_child = None
            for next_sorted_child_child in next_sorted_child.children:
                local_dist = calc_distance(sorted_child.center_latlng, next_sorted_child_child)
                if local_dist < min_dist:
                    min_dist = local_dist
                    nearest_child_child = next_sorted_child_child
            local_child_child.append(nearest_child_child)
        find_shortest_path_wrapper(local_child_child)


def calculate_route_wrapper(places):
    """
    This function is toppest function called by views.py
    :param places: Place object, need get corresponding Location, places[0] is begin point
    :return:
    """
    norm_points = [place for place in places]
    geo_tree = build_geo_tree(norm_points)
    find_shortest_path_wrapper(geo_tree)
    return geo_tree