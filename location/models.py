from __future__ import unicode_literals

from django.db import models
# from mongoengine.django.auth import User

from mongoengine import *


class Location(Document):
    name = StringField(max_length=60)
    latitude = DecimalField(precision=6, max_value=90)
    longitude = DecimalField(precision=6, max_value=180)
    # TODO: when query on latlng, ensure number over 180 are checked
    latlng = GeoPointField()
    address = StringField(max_length=80)
    placeId = StringField()


class Place(Document):
    alias = StringField(max_length=60)
    location = ReferenceField(Location)
    description = StringField(max_length=255, null=True, blank=True)
    # owner = models.ForeignKey(User, null=False)


class Locations(Document):
    locations = ListField(Location)


ZOOM_LEVEL = [
    {"level":1, "degree":"1"},
    {"level":2, "degree":"3"},
    {"level":3, "degree":"9"},
    {"level":4, "degree":"36"},
    {"level":5, "degree":"180"},
    {"level":6, "degree":"900"}
]


class Cluster(Document):
    level = IntField(min_value=1, max_value=6)
    center_lat = DecimalField(precision=6, max_value=90)
    center_lng = DecimalField(precision=6, max_value=180)
    center_latlng = GeoPointField()
    num_children = IntField()

    meta = {'allow_inheritance': True}


class LeafCluster(Cluster):
    locations = ListField(ReferenceField(Location))


class NodeCluster(Cluster):
    children = ListField(ReferenceField(Cluster))
    begin_child = ReferenceField(Cluster)
    path = ListField()


class Route(Document):
    # owner = ReferenceField(User)
    name = StringField(max_length=60)
    children = ListField(ReferenceField(Place))
    path = ReferenceField(Cluster)


# class Route(models.Model):
#
#     # 90.00 = 3x3x4x5x5x10
#     LEVEL_ONE = 10
#     LEVEL_TWO = 5
#     LEVEL_THREE = 5
#     LEVEL_FOUR = 4
#     LEVEL_FIVE = 3
#     LEVEL_SIX = 3
#
#     owner = models.ForeignKey(User)
#     locations = models.ManyToManyField(Location)
#     members = models.ManyToManyField(User)