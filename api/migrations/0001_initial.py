# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-07 16:05
from __future__ import unicode_literals

import api.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('photo', models.FileField(blank=True, default='avatar_default.jpg', null=True, upload_to='%Y/%m/%d/profile_pics')),
                ('bio', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('Parent', 'Parent'), ('Teacher', 'Teacher'), ('Student', 'Student'), ('Administrator', 'Administrator')], max_length=15)),
                ('receive_news', models.BooleanField(default=True)),
                ('twitter_handle', models.CharField(blank=True, max_length=25, null=True)),
                ('facebook_profile', models.TextField(blank=True, null=True)),
                ('linkedin_profile', models.TextField(blank=True, null=True)),
                ('website', models.TextField(blank=True, null=True)),
                ('telephone', models.CharField(blank=True, max_length=25, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AcademicsResultsLocalALevelOverall',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('result', models.CharField(max_length=8)),
                ('points', models.PositiveIntegerField(blank=True, null=True)),
                ('class_teacher_comment', models.TextField()),
                ('house_teacher_comment', models.TextField()),
                ('head_teacher_comment', models.TextField()),
            ],
            options={
                'verbose_name': 'A-level Overall Result',
                'db_table': 'academics_results_loc_a_overall',
            },
        ),
        migrations.CreateModel(
            name='AcademicsResultsLocalALevelSubject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('grade', models.CharField(max_length=2)),
                ('points', models.PositiveIntegerField(blank=True, null=True)),
                ('stream_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_position', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('type', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'A-level Subject Result',
                'db_table': 'academics_results_loc_a_subject',
            },
        ),
        migrations.CreateModel(
            name='AcademicsResultsLocalOLevelOverall',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('total_marks', models.CharField(max_length=4)),
                ('average_mark', models.CharField(max_length=4)),
                ('aggregate', models.PositiveIntegerField(blank=True, null=True)),
                ('division', models.CharField(max_length=3)),
                ('stream_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_teacher_comment', models.TextField()),
                ('house_teacher_comment', models.TextField()),
                ('head_teacher_comment', models.TextField()),
            ],
            options={
                'verbose_name': 'O-level Overall Result',
                'db_table': 'academics_results_loc_o_overall',
            },
        ),
        migrations.CreateModel(
            name='AcademicsResultsLocalOLevelSubject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('mark', models.CharField(max_length=6)),
                ('grade', models.CharField(max_length=2)),
                ('stream_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_position', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('type', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'O-level Subject Result',
                'db_table': 'academics_results_loc_o_subject',
            },
        ),
        migrations.CreateModel(
            name='AcademicsResultsLocalPrimaryOverall',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('total_marks', models.CharField(max_length=4)),
                ('average_mark', models.CharField(max_length=4)),
                ('aggregate', models.PositiveIntegerField(blank=True, null=True)),
                ('division', models.CharField(max_length=3)),
                ('stream_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_teacher_comment', models.TextField()),
                ('house_teacher_comment', models.TextField()),
                ('head_teacher_comment', models.TextField()),
            ],
            options={
                'verbose_name': 'Primary Overall Result',
                'db_table': 'academics_results_loc_p_overall',
            },
        ),
        migrations.CreateModel(
            name='AcademicsResultsLocalPrimarySubject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('result', models.CharField(max_length=3)),
                ('comment', models.TextField(blank=True, null=True)),
                ('type', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Primary Subject Result',
                'db_table': 'academics_results_loc_p_subject',
            },
        ),
        migrations.CreateModel(
            name='AcademicsResultsMarks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField()),
                ('term', models.PositiveIntegerField()),
                ('subject_paper', models.CharField(blank=True, max_length=3, null=True)),
                ('mark', models.CharField(max_length=6)),
                ('grade', models.CharField(max_length=2)),
                ('stream_position', models.PositiveIntegerField(blank=True, null=True)),
                ('class_position', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('type', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Student Mark',
                'db_table': 'academics_results_marks',
            },
        ),
        migrations.CreateModel(
            name='AssessmentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=25, null=True)),
                ('type', models.CharField(blank=True, choices=[('RAW', 'Raw'), ('WEIGHTED', 'Weighted'), ('AVERAGE', 'Average')], max_length=10, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('auto_compute', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, null=True)),
                ('auto_comment', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, null=True)),
            ],
            options={
                'db_table': 'assessment_types',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='%Y/%m/%d')),
                ('date', models.DateTimeField(auto_now=True)),
                ('content_type', models.CharField(blank=True, max_length=155, null=True)),
            ],
            options={
                'db_table': 'user_uploads',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('email_address', models.EmailField(max_length=254)),
                ('telephone', models.CharField(blank=True, max_length=12, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=10, null=True)),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_follows',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_likes',
            },
        ),
        migrations.CreateModel(
            name='Nok',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('occupation', models.CharField(blank=True, max_length=155, null=True)),
                ('relationship', models.CharField(blank=True, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Guardian', 'Guardian')], max_length=10, null=True)),
                ('nin', models.CharField(blank=True, max_length=20, null=True, verbose_name='National Identification Number')),
            ],
            options={
                'db_table': 'student_next_of_kin',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('details', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='ProfileSchool',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'profile_schools',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email_address', models.EmailField(blank=True, max_length=50, null=True)),
                ('telephone', models.CharField(blank=True, max_length=50, null=True)),
                ('physical_address', models.TextField(blank=True, null=True)),
                ('local_curriculum', models.BooleanField(default=False)),
                ('international_curriculum', models.BooleanField(default=False)),
                ('pre_primary_curriculum', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted')], default='INACTIVE', max_length=10, null=True)),
                ('validated', models.BooleanField(default=False)),
                ('registration_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'school_settings',
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('curriculum', models.CharField(blank=True, max_length=15, null=True)),
                ('level', models.CharField(blank=True, max_length=50, null=True)),
                ('level_short', models.CharField(blank=True, max_length=2, null=True)),
                ('name', models.CharField(default='S.1', max_length=20)),
                ('class_number', models.SmallIntegerField(blank=True, null=True)),
                ('stream', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'School Classes',
                'db_table': 'school_classes',
            },
        ),
        migrations.CreateModel(
            name='SchoolCommunication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
            ],
            options={
                'db_table': 'school_communications',
            },
        ),
        migrations.CreateModel(
            name='SchoolContactPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=20, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'school_contact_persons',
            },
        ),
        migrations.CreateModel(
            name='SchoolEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('all_day', models.CharField(blank=True, max_length=20, null=True)),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
            ],
            options={
                'db_table': 'school_events',
            },
        ),
        migrations.CreateModel(
            name='SchoolSubjectClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('compulsory', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_shares',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('surname', models.CharField(blank=True, max_length=15, null=True)),
                ('other_names', models.CharField(blank=True, max_length=15, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('initials', models.CharField(blank=True, max_length=5, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('Married', 'Married'), ('Single', 'Single')], max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('is_teacher', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, null=True)),
                ('mobile_telephone', models.CharField(blank=True, max_length=12, null=True)),
                ('alternative_telephone', models.CharField(blank=True, max_length=12, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
            ],
            options={
                'db_table': 'staff_general',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('admission_number', models.CharField(blank=True, max_length=35, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2)),
                ('nationality', models.CharField(blank=True, max_length=20, null=True)),
                ('other_info', models.TextField(blank=True, null=True)),
                ('nin', models.CharField(blank=True, max_length=20, null=True, verbose_name='National Identification Number')),
                ('photo', models.FileField(default='avatar_default.jpg', upload_to=api.models.student_photo_directory)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
                ('school_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass')),
            ],
            options={
                'db_table': 'student_general',
            },
        ),
        migrations.CreateModel(
            name='StudentNok',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'students_and_nok',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(blank=True, max_length=5, null=True)),
                ('code', models.CharField(blank=True, max_length=12, null=True)),
                ('curriculum', models.CharField(blank=True, max_length=15, null=True)),
                ('group', models.CharField(blank=True, max_length=5, null=True)),
                ('area', models.CharField(blank=True, max_length=40, null=True)),
                ('standard', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, null=True)),
                ('level', models.CharField(blank=True, choices=[('Primary', 'Primary'), ('O level', 'O level'), ('A level', 'A level')], max_length=4, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('principal_subsidiary', models.CharField(blank=True, choices=[('P', 'Principal'), ('S', 'Subsidiary'), ('N', 'None')], max_length=1, null=True)),
                ('report_mark_grade', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
            ],
            options={
                'db_table': 'school_subjects',
            },
        ),
        migrations.CreateModel(
            name='SubjectGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.CharField(blank=True, choices=[('Primary', 'Primary'), ('O level', 'O level'), ('A level', 'A level')], max_length=1, null=True)),
                ('group', models.CharField(blank=True, max_length=5, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
            ],
            options={
                'db_table': 'school_subject_groups',
            },
        ),
        migrations.CreateModel(
            name='SubjectPaper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('paper', models.IntegerField()),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Subject')),
            ],
            options={
                'db_table': 'school_subject_papers',
            },
        ),
        migrations.AddField(
            model_name='schoolsubjectclass',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Subject'),
        ),
        migrations.AddField(
            model_name='schoolsubjectclass',
            name='subject_paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SubjectPaper'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='class_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Staff'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='profileschool',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='profileschool',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='nok',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='nok',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='nok',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Post'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Post'),
        ),
        migrations.AddField(
            model_name='assessmenttype',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultsmarks',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultsmarks',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultsmarks',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultsmarks',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='academicsresultsmarks',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Subject'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimarysubject',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimarysubject',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimarysubject',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimarysubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimarysubject',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Subject'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimaryoverall',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimaryoverall',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimaryoverall',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalprimaryoverall',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalolevelsubject',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalolevelsubject',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalolevelsubject',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalolevelsubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalolevelsubject',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Subject'),
        ),
        migrations.AddField(
            model_name='academicsresultslocaloleveloverall',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultslocaloleveloverall',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocaloleveloverall',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocaloleveloverall',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalalevelsubject',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalalevelsubject',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalalevelsubject',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalalevelsubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalalevelsubject',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Subject'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalaleveloverall',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalaleveloverall',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SchoolClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalaleveloverall',
            name='school_subject_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.SchoolSubjectClass'),
        ),
        migrations.AddField(
            model_name='academicsresultslocalaleveloverall',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
    ]
