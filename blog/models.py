from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=60)
    def __unicode__(self):
        return self.name

class Log(models.Model):
    title = models.CharField(max_length=60)
    project = models.ForeignKey(Project, null=False)
    date = models.DateTimeField(default=timezone.now)
    question = models.TextField(max_length=1000, null=True)
    content = models.TextField(max_length=15000)
    def __unicode__(self):
        return self.title