# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0006_merge_20170802_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=35, verbose_name='Colonia'),
        ),
    ]
