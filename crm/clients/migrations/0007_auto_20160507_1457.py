# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-07 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20160428_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='legal_details',
            name='address',
            field=models.CharField(default=str, max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billing',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Account'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client_contacts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.ClientContactDetails'),
        ),
    ]
