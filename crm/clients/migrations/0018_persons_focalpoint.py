# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-24 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_clientcontactdetails_focalpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='focalPoint',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
