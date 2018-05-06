# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-27 01:10
from __future__ import unicode_literals

from django.db import migrations
from decimal import Decimal


missing_postal_codes = [
	# ('67480',25.8669,-100.007,'Nuevo Leon'),
	('23410',26.8167,-112.4167,'Baja California Sur')
]

def create_values(apps, schema_editor):
    Carrier = apps.get_model('logistics', 'Carrier')
    PostalCode = apps.get_model('logistics', 'PostalCode')
    State = apps.get_model('logistics', 'State')
    db_alias = schema_editor.connection.alias
    dhl, _created = Carrier.objects.using(db_alias).get_or_create(name='DHL')

    states = State.objects.using(db_alias).all()
    states_dict = {state.name: state for state in states}
    for postal_info in missing_postal_codes:
        info = { 'code':postal_info[0],
                 'latitude': Decimal(postal_info[1]),
                 'longitude': Decimal(postal_info[2]),
                 'state': states_dict[postal_info[3]]}
        postal_code, _created = PostalCode.objects.using(db_alias).get_or_create(**info)

def remove_values(apps, schema_editor):
	Carrier = apps.get_model('logistics', 'Carrier')
	PostalCode = apps.get_model('logistics', 'PostalCode')
	db_alias = schema_editor.connection.alias
	Carrier.objects.using(db_alias).get(name='DHL').delete()
	for postal_info in missing_postal_codes:
		PostalCode.objects.using(db_alias).filter(code=postal_info[0]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0013_auto_20171014_2156'),
    ]

    operations = [
	    migrations.RunPython(create_values,remove_values),
    ]