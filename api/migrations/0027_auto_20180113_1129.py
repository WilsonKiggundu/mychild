# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-13 08:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20180113_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolcontactperson',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]