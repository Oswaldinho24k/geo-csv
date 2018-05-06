# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-27 01:09
from __future__ import unicode_literals

from django.db import migrations

def create_entity(apps, schema_editor):
    Entity = apps.get_model('waypoints', 'Entity')
    WaypointGroup = apps.get_model('waypoints', 'WaypointGroup')
    db_alias = schema_editor.connection.alias
    dhl, created = Entity.objects.using(db_alias).get_or_create(name='DHL')
    god_group = WaypointGroup.objects.using(db_alias).get(name='Todos')
    if created:
        god_group.entities.add(dhl)
    god_group.save()

def remove_entity(apps, schema_editor):
	Entity = apps.get_model('waypoints', 'Entity')
	db_alias = schema_editor.connection.alias
    # It's not cool to delete all entities when there are still points that need them.
	# Entity.objects.using(db_alias).get(name='Fedex').delete()
	# Entity.objects.using(db_alias).get(name='Estafeta').delete()
	Entity.objects.using(db_alias).get(name='DHL').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0025_create_base_entities'),
    ]

    operations = [
	    migrations.RunPython(create_entity,remove_entity),
    ]
