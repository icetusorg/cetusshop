# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-06 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0020_auto_20171204_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruit',
            name='page_title',
        ),
        migrations.RemoveField(
            model_name='recruit',
            name='short_desc',
        ),
        migrations.RemoveField(
            model_name='recruit',
            name='static_file_name',
        ),
        migrations.AddField(
            model_name='recruit',
            name='education',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='学历要求'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='number',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='招聘人数'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='site',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='工作地点'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='type',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='工作类型'),
        ),
        migrations.AlterField(
            model_name='recruit',
            name='title',
            field=models.CharField(db_index=True, max_length=254, null=True, verbose_name='岗位名称'),
        ),
    ]
