# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-20 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0032_auto_20160803_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='focalPoint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.Persons'),
        ),
    ]