# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-13 23:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_auto_20160513_2225'),
    ]

    operations = [
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
