# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-21 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0033_order_focalpoint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='focalPoint',
            new_name='contactPerson',
        ),
    ]