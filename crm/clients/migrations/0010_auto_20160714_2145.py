# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-14 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20160713_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcontactdetails',
            name='addedAt',
            field=models.DateField(auto_now_add=True),
        ),
    ]