# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-28 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0011_auto_20170901_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaypointGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del Grupo')),
                ('waypoints', models.ManyToManyField(blank=True, to='waypoints.Waypoint')),
            ],
        ),
    ]
