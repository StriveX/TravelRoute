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

    def __unicode__(self):
        return self.name