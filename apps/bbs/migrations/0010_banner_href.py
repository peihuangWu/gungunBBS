# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-28 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0009_auto_20200428_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='href',
            field=models.TextField(default='/index/', verbose_name='链接'),
        ),
    ]
