# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 04:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('date', models.DateTimeField(default=datetime.datetime(2016, 3, 29, 4, 42, 46, 280161))),
                ('question', models.TextField(max_length=1000, null=True)),
                ('content', models.TextField(max_length=15000)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Project'),
        ),
    ]