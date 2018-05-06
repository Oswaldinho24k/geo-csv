# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 06:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0007_auto_20170713_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='billing_phone',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='El número de telefono tiene que tener el siguiente formato: "+999999999" El número tiene que tener entre 9 y 15 dígitos.', regex='^\\+?1?\\d{7,15}$')], verbose_name='Teléfono de Facturación'),
        ),
        migrations.AlterField(
            model_name='client',
            name='commercial_contact_phone',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='El número de telefono tiene que tener el siguiente formato: "+999999999" El número tiene que tener entre 9 y 15 dígitos.', regex='^\\+?1?\\d{7,15}$')], verbose_name='Teléfono del Contacto Comercial'),
        ),
    ]
