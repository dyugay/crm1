# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-03 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0031_auto_20160803_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persons',
            name='email1',
            field=models.EmailField(default=b'', max_length=254),
        ),
        migrations.AlterField(
            model_name='persons',
            name='email2',
            field=models.EmailField(default=b'', max_length=254),
        ),
        migrations.AlterField(
            model_name='persons',
            name='telephoneNum3',
            field=models.CharField(default=b'', max_length=16),
        ),
    ]
