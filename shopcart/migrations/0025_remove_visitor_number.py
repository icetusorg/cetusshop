# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-08 08:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0024_auto_20171208_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='number',
        ),
    ]
