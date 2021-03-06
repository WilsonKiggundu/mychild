# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-30 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='path',
        ),
        migrations.AddField(
            model_name='attachment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='posts/attachments/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='post',
            name='viewers',
            field=models.CharField(default='1', max_length=155),
        ),
    ]
