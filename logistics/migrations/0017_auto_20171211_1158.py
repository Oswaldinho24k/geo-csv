# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-11 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0016_auto_20171211_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postalcode',
            name='longitude',
            field=models.DecimalField(decimal_places=22, max_digits=25, verbose_name='Longitud'),
        ),
    ]