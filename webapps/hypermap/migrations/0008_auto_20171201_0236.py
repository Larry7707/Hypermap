# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-01 07:36
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hypermap', '0007_auto_20171201_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='last_changed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 1, 2, 36, 0, 508980)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
