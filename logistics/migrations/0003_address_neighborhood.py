# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0002_load_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(default='Los Girasoles', max_length=35, verbose_name='Colonia'),
            preserve_default=False,
        ),
    ]