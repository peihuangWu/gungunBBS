# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-19 12:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, verbose_name='昵称')),
                ('type', models.CharField(default='live', max_length=20, verbose_name='分区')),
                ('publish_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发布时间')),
                ('click_num', models.IntegerField(default=0, verbose_name='浏览数')),
                ('reply_num', models.IntegerField(default=0, verbose_name='回复数')),
                ('content', models.TextField(default='', verbose_name='内容')),
            ],
            options={
                'verbose_name': '帖子信息',
                'verbose_name_plural': '帖子信息',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发布时间')),
                ('content', models.TextField(default='', verbose_name='内容')),
            ],
            options={
                'verbose_name': '回复信息',
                'verbose_name_plural': '回复信息',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='', max_length=30, verbose_name='昵称')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs.User', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='reply',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs.Post', verbose_name='帖子'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs.User', verbose_name='作者'),
        ),
    ]
