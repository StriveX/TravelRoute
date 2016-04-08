from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mongoengine import *


class Location(Document):
    name = StringField(max_length=60)
    latitude = DecimalField(precision=6, max_value=90)
    longitude = DecimalField(precision=6, max_value=180)
    address = StringField(max_length=80)
    # description = StringField(max_length=255, null=True, blank=True)
    # owner = models.ForeignKey(User, null=False)

class Place(Document):
    alias = StringField(max_length=60)
    location = ReferenceField(Location)

class Locations(Document):
    locations = ListField(Location)

class Cluster(models.Model):
    level = models.PositiveSmallIntegerField(null=False)
    # center_lat = models.DecimalField(max_digits=10, decimal_places=6)
    # center_lng = models.DecimalField(max_digits=10, decimal_places=6)
    center_lat = DecimalField(precision=6, max_value=90)
    center_lng = DecimalField(precision=6, max_value=180)
    num_children = IntField()

    def __unicode__(self):
        return self.name

class LeafCluster(Cluster):

class NodeCluster(Cluster)

class Route(Document):

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