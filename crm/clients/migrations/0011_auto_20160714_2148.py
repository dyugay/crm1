# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-14 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20160714_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legal_details',
            name='addedAt',
            field=models.DateField(auto_now_add=True),
        ),
    ]