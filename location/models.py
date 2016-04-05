from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=60)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    #radius
    #tag
    #type (eat, view ...)
    address = models.CharField(max_length=80)
    description = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(User, null=False)


class Cluster(models.Model):
    level = models.PositiveSmallIntegerField(null=False)
    center_lat = models.DecimalField(max_digits=10, decimal_places=6)
    center_lng = models.DecimalField(max_digits=10, decimal_places=6)
    num_children = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

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