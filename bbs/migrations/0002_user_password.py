# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-19 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=30, verbose_name='密码'),
        ),
    ]
