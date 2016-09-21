# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-17 20:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0013_auto_20160715_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=20)),
                ('middleName', models.CharField(max_length=20)),
                ('telephoneNum1', models.CharField(max_length=16, null=True)),
                ('telephoneNum2', models.CharField(max_length=16, null=True)),
                ('telephoneNum3', models.CharField(max_length=16, null=True)),
                ('email1', models.EmailField(max_length=254, null=True)),
                ('email2', models.EmailField(max_length=254, null=True)),
                ('changedOn', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
            ],
        ),
    ]