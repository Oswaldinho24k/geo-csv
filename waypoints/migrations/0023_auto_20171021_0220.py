# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-21 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0022_migrate_external_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waypoint',
            name='external_id',
            field=models.CharField(max_length=35, unique=True, verbose_name='Id del Punto en API Externa'),
        ),
    ]
