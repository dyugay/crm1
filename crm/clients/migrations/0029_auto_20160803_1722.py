# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-03 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0028_auto_20160801_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='manager',
        ),
        migrations.AlterField(
            model_name='client',
            name='addedAt',
            field=models.DateField(auto_now=True),
        ),
    ]
