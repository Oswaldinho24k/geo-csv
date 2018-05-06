# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-11 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0015_externalshipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postalcode',
            name='latitude',
            field=models.DecimalField(decimal_places=22, max_digits=25, verbose_name='Latitud'),
        ),
    ]