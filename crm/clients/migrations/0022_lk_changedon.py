# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-30 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_lk'),
    ]

    operations = [
        migrations.AddField(
            model_name='lk',
            name='changedOn',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
