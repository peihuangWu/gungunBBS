# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-04 10:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0013_topic_topicfollow_topicpost_topicreply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicreply',
            name='topic',
        ),
        migrations.AddField(
            model_name='topicreply',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs.TopicPost', verbose_name='帖子'),
        ),
    ]
