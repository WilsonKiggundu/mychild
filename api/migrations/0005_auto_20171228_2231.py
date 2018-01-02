# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-28 19:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20171228_2227'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='assessmenttype',
            table='assessment_types',
        ),
        migrations.AlterModelTable(
            name='nok',
            table='student_next_of_kin',
        ),
        migrations.AlterModelTable(
            name='profile',
            table='mychild_profiles',
        ),
        migrations.AlterModelTable(
            name='schoolclass',
            table='school_classes',
        ),
        migrations.AlterModelTable(
            name='schoolcommunication',
            table='school_communications',
        ),
        migrations.AlterModelTable(
            name='schoolcontactperson',
            table='school_contact_persons',
        ),
        migrations.AlterModelTable(
            name='schoolevent',
            table='school_events',
        ),
        migrations.AlterModelTable(
            name='staff',
            table='staff_general',
        ),
        migrations.AlterModelTable(
            name='student',
            table='student_general',
        ),
        migrations.AlterModelTable(
            name='subject',
            table='school_subjects',
        ),
        migrations.AlterModelTable(
            name='subjectgroup',
            table='school_subject_groups',
        ),
        migrations.AlterModelTable(
            name='subjectpaper',
            table='school_subject_papers',
        ),
    ]