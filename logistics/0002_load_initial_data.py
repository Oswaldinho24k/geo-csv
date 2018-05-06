# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from iupick.settings.base import BASE_DIR
from django.db import migrations
from logistics.models import Carrier, Country, State, PostalCode
from decimal import Decimal

CARRIERS = [
    'Fedex',
    'Estafeta',
]


def forwards_func(apps, schema_editor):
    """ Create all the required groups in the database.

    """
    # print(os.pwd())
    csv_directory = BASE_DIR + '/../logistics/data_csv/'
    states = []
    postal_dict = {}
    with open(csv_directory + 'mx_state_code.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            states.append({'name': row[0], 'code': row[1]})
    with open(csv_directory + 'mx_postal_codes.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            state = row[1]
            if state not in postal_dict.keys():
                postal_dict[state] = []
            postal_dict[state].append({'code': row[0],
                                       'latitude': row[3],
                                       'longitude': row[4]})
    db_alias = schema_editor.connection.alias
    for carrier in CARRIERS:
        Carrier.objects.using(db_alias).create(name=carrier)
    mexico, _ = Country.objects.using(db_alias).get_or_create({'name': 'México',
                                                               'code': 'MX'})
    state_models = []
    for state in states:
        state_model = State(country=mexico, name=state['name'], code=state['code'])
        state_models.append(state_model)
    state_models = State.objects.using(db_alias).bulk_create(state_models)
    postal_models = []
    for state in state_models:
        for postal_code in postal_dict[state.name]:
            postal_model = PostalCode(code=postal_code['code'],
                                      latitude=Decimal(postal_code['latitude']),
                                      longitude=Decimal(postal_code['longitude']),
                                      state=state)
            postal_models.append(postal_model)
    postal_models = PostalCode.objects.using(db_alias).bulk_create(postal_models)


def reverse_func(apps, schema_editor):
    """ Revert changes made in forwards_func
    """
    db_alias = schema_editor.connection.alias
    for carrier in CARRIERS:
        Carrier.objects.using(db_alias).filter(name=carrier).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
