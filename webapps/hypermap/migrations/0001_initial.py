# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 14:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('content', models.CharField(max_length=420)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_to', models.CharField(choices=[('PR', 'private'), ('FR', 'friends'), ('GL', 'global')], default='PR', max_length=2)),
                ('post_time', models.DateTimeField()),
                ('lat', models.DecimalField(decimal_places=5, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=5, max_digits=10)),
                ('title', models.CharField(max_length=42)),
                ('description', models.CharField(max_length=420)),
                ('image', models.ImageField(default='hypermap/static/hypermap/media/default_event.jpg', max_length=500, upload_to='hypermap/static/hypermap/media')),
                ('contact_info', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='hypermap/static/hypermap/media/default_profile.jpg', upload_to='hypyermap/static/hypermap/media')),
                ('confirmed', models.BooleanField(default=False)),
                ('friends', models.ManyToManyField(related_name='_profile_friends_+', to='hypermap.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('news_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hypermap.News')),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('register_required', models.BooleanField(default=False)),
                ('registered', models.ManyToManyField(related_name='registered_event', to='hypermap.Profile')),
            ],
            bases=('hypermap.news',),
        ),
        migrations.CreateModel(
            name='Help',
            fields=[
                ('news_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hypermap.News')),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('solved', models.BooleanField(default=False)),
            ],
            bases=('hypermap.news',),
        ),
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.ManyToManyField(related_name='liked_event', to='hypermap.Profile'),
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hypermap.News'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]