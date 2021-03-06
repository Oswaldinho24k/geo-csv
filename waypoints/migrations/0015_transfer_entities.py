# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-17 19:25
from __future__ import unicode_literals

from django.db import migrations

def link_entities(apps, schema_editor):
    Waypoint = apps.get_model('waypoints', 'Waypoint')
    Entity = apps.get_model('waypoints', 'Entity')
    db_alias = schema_editor.connection.alias
    for waypoint in Waypoint.objects.all():
        entity, created = Entity.objects.using(db_alias).get_or_create(name=waypoint.entity)
        waypoint.entity_link = entity
        waypoint.save()

def delink_entities(apps, schema_editor):
    Waypoint = apps.get_model('waypoints', 'Waypoint')
    Entity = apps.get_model('waypoints', 'Entity')
    db_alias = schema_editor.connection.alias
    for waypoint in Waypoint.objects.using(db_alias).all():
        waypoint.entity = waypoint.entity_link
        waypoint.entity_link = None
        waypoint.save()

class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0014_auto_20171017_1924'),
    ]

    operations = [
	    migrations.RunPython(link_entities,delink_entities),
    ]