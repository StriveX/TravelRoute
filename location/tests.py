from django.test import TestCase

# Create your tests here.


from .models import *
from utils import insert_into_geo_tree
import pdb


def insert_into_geo_tree_test():
    # children_ids = ["5709fcacd7c3f263bdcd468d",
    #                 "5709fcc6d7c3f263bdcd468e"]
    # points = Place.objects(id__in=children_ids).only('id', 'location')
    points = Place.objects.only('id', 'location')
    print points
    geo_tree = NodeCluster(center_latlng=points[0].location.latlng, level=6, num_children=0, num_locations=0)
    for i in range(len(points)):
        insert_into_geo_tree(points[i], geo_tree, 6)
    geo_tree.print_cluster()
    return geo_tree

