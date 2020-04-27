# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-25 20:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usersystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfollow',
            name='follower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='be_follow_user', to=settings.AUTH_USER_MODEL, verbose_name='被关注者'),
        ),
        migrations.AlterField(
            model_name='userfollow',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
