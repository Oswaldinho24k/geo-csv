# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.FloatField()),
                ('tracking_number', models.CharField(blank=True, max_length=255)),
                ('waybill_link', models.URLField(max_length=500)),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.Carrier')),
                ('recipient_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_address', to='logistics.Address')),
            ],
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_extension',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AddField(
            model_name='shipment',
            name='recipient_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_contact', to='logistics.Contact'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='shipper_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipper_address', to='logistics.Address'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='shipper_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipper_contact', to='logistics.Contact'),
        ),
    ]