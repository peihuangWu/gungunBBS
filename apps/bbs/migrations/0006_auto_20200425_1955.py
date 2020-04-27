# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-25 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0005_remove_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_month',
            field=models.IntegerField(default=1, verbose_name='出生月份'),
        ),
        migrations.AddField(
            model_name='user',
            name='birth_year',
            field=models.IntegerField(default=1990, verbose_name='出生年份'),
        ),
        migrations.AddField(
            model_name='user',
            name='college',
            field=models.CharField(default='电气工程学院', max_length=40, verbose_name='所在学院'),
        ),
        migrations.AddField(
            model_name='user',
            name='emotion',
            field=models.CharField(default='单身', max_length=10, verbose_name='情感状态'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='男', max_length=5, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='user',
            name='portrait',
            field=models.TextField(default='data:image/png;base64,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', verbose_name='用户头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='sign',
            field=models.TextField(default='', verbose_name='个性签名'),
        ),
    ]
