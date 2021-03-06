# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=35, verbose_name='Municipio/Delegación')),
                ('line_one', models.CharField(max_length=35, verbose_name='Dirección 1')),
                ('line_two', models.CharField(blank=True, max_length=35, verbose_name='Dirección 2')),
            ],
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, verbose_name='Nombre del Transportista')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, verbose_name='Pais')),
                ('code', models.CharField(max_length=2, verbose_name='Codigo de Pais')),
            ],
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, verbose_name='Codigo Postal')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Latitud')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Longitud')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, verbose_name='Estado')),
                ('code', models.CharField(max_length=2, verbose_name='Codigo de Estado (2 letras)')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.Country')),
            ],
        ),
        migrations.AddField(
            model_name='postalcode',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.PostalCode'),
        ),
    ]
