# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-13 05:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20180112_1630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicsresultslocalaleveloverall',
            options={'verbose_name': 'A-level Overall Result'},
        ),
        migrations.AlterModelOptions(
            name='academicsresultslocalalevelsubject',
            options={'verbose_name': 'A-level Subject Result'},
        ),
        migrations.AlterModelOptions(
            name='academicsresultslocaloleveloverall',
            options={'verbose_name': 'O-level Overall Result'},
        ),
        migrations.AlterModelOptions(
            name='academicsresultslocalolevelsubject',
            options={'verbose_name': 'O-level Subject Result'},
        ),
        migrations.AlterModelOptions(
            name='academicsresultslocalprimaryoverall',
            options={'verbose_name': 'Primary Overall Result'},
        ),
        migrations.AlterModelOptions(
            name='academicsresultslocalprimarysubject',
            options={'verbose_name': 'Primary Subject Result'},
        ),
        migrations.AlterModelOptions(
            name='academicsresultsmarks',
            options={'verbose_name': 'Student Mark'},
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='curriculum_specific',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='next_term_end',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='next_term_start',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='progression',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='term',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='term_end',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='term_start',
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='year',
        ),
    ]