# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-24 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0018_persons_focalpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persons',
            name='focalPoint',
            field=models.BooleanField(default=False),
        ),
    ]