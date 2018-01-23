# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-16 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20180113_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsfeed',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newsfeed',
            name='type',
            field=models.CharField(blank=True, choices=[('Event', 'Event'), ('Blog', 'Blog'), ('Marks', 'Marks'), ('Media', 'Media')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
    ]