# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-28 19:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20171228_2224'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='school',
            table='school_settings',
        ),
    ]
