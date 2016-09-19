# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-15 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_auto_20160714_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email1',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='email2',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='firstName',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='lastName',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='middleName',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='telephoneNum1',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='telephoneNum2',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='telephoneNum3',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
