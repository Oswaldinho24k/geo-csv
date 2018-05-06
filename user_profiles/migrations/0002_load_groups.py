# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import Group
from user_profiles.utils import ADMIN_GROUP, CLIENT_GROUP

def forwards_func(apps, schema_editor):
    """ Create all the required groups in the database.

    """
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).get_or_create(name=ADMIN_GROUP)
    Group.objects.using(db_alias).get_or_create(name=CLIENT_GROUP)

def reverse_func(apps, schema_editor):
    """ Revert changes made in forwards_func
    """
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name=ADMIN_GROUP).delete()
    Group.objects.using(db_alias).filter(name=CLIENT_GROUP).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]