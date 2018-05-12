# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-01 07:01
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hypermap', '0005_auto_20171130_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='content',
            field=models.CharField(default='', max_length=420),
        ),
        migrations.AddField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 1, 2, 1, 39, 572057)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
