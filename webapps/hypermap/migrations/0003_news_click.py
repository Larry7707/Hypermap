# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-16 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hypermap', '0002_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='click',
            field=models.IntegerField(default=0),
        ),
    ]