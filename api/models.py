from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from api.options import *


def student_photo_directory(instance, filename):
    return 'students/%s/photos/%s' % (instance.user.profile.school.id, filename)


class School(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    telephone = models.CharField(max_length=50, blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    local_curriculum = models.CharField(choices=YES_NO, default='N', max_length=1, null=True, blank=True)
    international_curriculum = models.CharField(choices=YES_NO, default='N', max_length=1, null=True, blank=True)
    pre_primary_curriculum = models.CharField(choices=YES_NO, default='N', max_length=1, null=True, blank=True)
    status = models.CharField(choices=STATUS, default='INACTIVE', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'school_settings'


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True


class AssessmentType(BaseModel):
    order = models.IntegerField()
    name = models.CharField(max_length=25, null=True, blank=True)
    type = models.CharField(max_length=10, choices=ASSESSMENT_TYPES, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    auto_compute = models.CharField(max_length=1, choices=YES_NO, null=True, blank=True)
    auto_comment = models.CharField(max_length=1, choices=YES_NO, null=True, blank=True)

    class Meta:
        db_table = 'assessment_types'


class Subject(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    short = models.CharField(max_length=5, null=True, blank=True)
    code = models.CharField(max_length=12, null=True, blank=True)
    curriculum = models.CharField(max_length=15, null=True, blank=True)
    group = models.CharField(max_length=5, null=True, blank=True)
    area = models.CharField(max_length=40, null=True, blank=True)
    standard = models.CharField(choices=YES_NO, max_length=1, null=True, blank=True)
    level = models.CharField(choices=CURRICULUM_LEVELS, max_length=4, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    principal_subsidiary = models.CharField(choices=PRINCIPAL_SUBSIDIARY, max_length=1, null=True, blank=True)
    report_mark_grade = models.CharField(choices=YES_NO, max_length=1, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'school_subjects'


class SubjectGroup(BaseModel):
    level = models.CharField(choices=CURRICULUM_LEVELS, max_length=1, null=True, blank=True)
    group = models.CharField(max_length=5, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'school_subject_groups'


class SubjectPaper(BaseModel):
    paper = models.IntegerField()
    code = models.CharField(max_length=10, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'school_subject_papers'


class Staff(BaseModel):
    surname = models.CharField(max_length=15, null=True, blank=True)
    other_names = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=1, null=True, blank=True)
    title = models.CharField(max_length=20, null=True, blank=True)
    initials = models.CharField(max_length=5, null=True, blank=True)
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    is_teacher = models.CharField(choices=YES_NO, max_length=1, null=True, blank=True)
    mobile_telephone = models.CharField(max_length=12, null=True, blank=True)
    alternative_telephone = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        db_table = 'staff_general'


class Profile(BaseModel):
    photo = models.FileField(upload_to='%Y/%m/%d/profile_pics', default='avatar_default.jpg', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    type = models.CharField(choices=PROFILE_TYPE, max_length=15, blank=False, null=False)
    child_code = models.CharField(max_length=12, blank=False, null=False)
    receive_news = models.BooleanField(default=True)
    twitter_handle = models.CharField(max_length=25, null=True, blank=True)
    facebook_profile = models.TextField(null=True, blank=True)
    linkedin_profile = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=25, null=True, blank=True)
    website = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        db_table = 'user_profiles'


class SchoolCommunication(BaseModel):
    sender = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'school_communications'


class SchoolEvent(BaseModel):
    type = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'school_events'


class SchoolClass(BaseModel):
    curriculum = models.CharField(max_length=15, null=True, blank=True)
    # curriculum_specific = models.CharField(max_length=100, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    level_short = models.CharField(max_length=2, null=True, blank=True)
    # progression = models.IntegerField()
    name = models.CharField(max_length=20, default='S.1', null=False, blank=False)
    class_number = models.SmallIntegerField(null=True, blank=True)
    stream = models.CharField(max_length=30, null=True, blank=True)
    class_teacher = models.ForeignKey(Staff, null=True, blank=True)

    # year = models.CharField(max_length=9, null=True, blank=True)
    # term = models.SmallIntegerField()
    # term_start = models.DateTimeField()
    # term_end = models.DateTimeField()
    # next_term_start = models.DateTimeField()
    # next_term_end = models.DateTimeField()
    # stage = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.name, self.stream)

    class Meta:
        verbose_name_plural = 'School Classes'
        db_table = 'school_classes'


class Student(BaseModel):
    code = models.CharField(max_length=15, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=25, blank=False, null=False)
    last_name = models.CharField(max_length=25, blank=False, null=False)
    admission_number = models.CharField(max_length=35, null=True, blank=True)
    school_class = models.ForeignKey(SchoolClass, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER, blank=False, null=False)
    nationality = models.CharField(max_length=20, null=True, blank=True)
    other_info = models.TextField(null=True, blank=True)
    nin = models.CharField(max_length=20, null=True, blank=True, verbose_name="National Identification Number")
    photo = models.FileField(upload_to=student_photo_directory, default='avatar_default.jpg')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        db_table = 'student_general'


class Nok(BaseModel):
    occupation = models.CharField(max_length=155, null=True, blank=True)
    relationship = models.CharField(choices=NOK_TYPE, max_length=10, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    nin = models.CharField(max_length=20, null=True, blank=True, verbose_name="National Identification Number")

    class Meta:
        db_table = 'student_next_of_kin'


class StudentNok(BaseModel):
    student = models.ForeignKey(Student)
    profile = models.ForeignKey(Profile)

    class Meta:
        db_table = "students_and_nok"


class SchoolContactPerson(BaseModel):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'school_contact_persons'


class Post(BaseModel):
    details = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.details

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        db_table = 'posts'


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='%Y/%m/%d', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=155, null=True, blank=True)

    class Meta:
        db_table = 'user_uploads'


class Comment(models.Model):
    post = models.ForeignKey(Post)
    comment = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#%s' % self.id


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_likes'


class Share(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_shares'


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_follows'


class SchoolSubjectClass(BaseModel):
    school_class = models.ForeignKey(SchoolClass)
    subject = models.ForeignKey(Subject)
    subject_paper = models.ForeignKey(SubjectPaper)
    compulsory = models.CharField(choices=YES_NO, max_length=1)


class ResultsBaseModel(BaseModel):
    student = models.ForeignKey(Student, null=False, blank=False)
    year = models.PositiveIntegerField(null=False, blank=False)
    term = models.PositiveIntegerField(null=False, blank=False)
    school_subject_class = models.ForeignKey(SchoolSubjectClass, null=True, blank=True)
    school_class = models.ForeignKey(SchoolClass, null=False, blank=False)

    class Meta:
        abstract = True


class AcademicsResultsLocalPrimarySubject(ResultsBaseModel):
    result = models.CharField(max_length=3)
    comment = models.TextField(null=True, blank=True)
    type = models.PositiveSmallIntegerField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)

    class Meta:
        verbose_name = "Primary Subject Result"
        db_table = 'academics_results_loc_p_subject'


class AcademicsResultsMarks(ResultsBaseModel):
    subject_paper = models.CharField(max_length=3, null=True, blank=True)
    mark = models.CharField(max_length=6)
    grade = models.CharField(max_length=2)
    stream_position = models.PositiveIntegerField(null=True, blank=True)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField()
    type = models.PositiveSmallIntegerField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)

    class Meta:
        verbose_name = "Student Mark"
        db_table = 'academics_results_marks'


class AcademicsResultsLocalPrimaryOverall(ResultsBaseModel):
    total_marks = models.CharField(max_length=4)
    average_mark = models.CharField(max_length=4)
    aggregate = models.PositiveIntegerField(blank=True, null=True)
    division = models.CharField(max_length=3)
    stream_position = models.PositiveIntegerField(null=True, blank=True)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    class_teacher_comment = models.TextField()
    house_teacher_comment = models.TextField()
    head_teacher_comment = models.TextField()

    class Meta:
        verbose_name = "Primary Overall Result"
        db_table = 'academics_results_loc_p_overall'


class AcademicsResultsLocalOLevelSubject(ResultsBaseModel):
    mark = models.CharField(max_length=6)
    grade = models.CharField(max_length=2)
    stream_position = models.PositiveIntegerField(null=True, blank=True)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField()
    type = models.PositiveSmallIntegerField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)

    class Meta:
        verbose_name = "O-level Subject Result"
        db_table = 'academics_results_loc_o_subject'


class AcademicsResultsLocalOLevelOverall(ResultsBaseModel):
    total_marks = models.CharField(max_length=4)
    average_mark = models.CharField(max_length=4)
    aggregate = models.PositiveIntegerField(blank=True, null=True)
    division = models.CharField(max_length=3)
    stream_position = models.PositiveIntegerField(null=True, blank=True)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    class_teacher_comment = models.TextField()
    house_teacher_comment = models.TextField()
    head_teacher_comment = models.TextField()

    class Meta:
        verbose_name = "O-level Overall Result"
        db_table = 'academics_results_loc_o_overall'


class AcademicsResultsLocalALevelSubject(ResultsBaseModel):
    grade = models.CharField(max_length=2)
    points = models.PositiveIntegerField(null=True, blank=True)
    stream_position = models.PositiveIntegerField(null=True, blank=True)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField()
    type = models.PositiveSmallIntegerField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)

    class Meta:
        verbose_name = "A-level Subject Result"
        db_table = 'academics_results_loc_a_subject'


class AcademicsResultsLocalALevelOverall(ResultsBaseModel):
    result = models.CharField(max_length=8)
    points = models.PositiveIntegerField(blank=True, null=True)
    class_teacher_comment = models.TextField()
    house_teacher_comment = models.TextField()
    head_teacher_comment = models.TextField()

    class Meta:
        verbose_name = "A-level Overall Result"
        db_table = 'academics_results_loc_a_overall'


class Employee(models.Model):
    first_name = models.CharField(max_length=25, null=False, blank=False)
    email_address = models.EmailField()
    telephone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)

    class Meta:
        db_table = "employees"

# class AcademicsResultsIntPrimarySubject(ResultsBaseModel):
#     class Meta:
#         db_table = 'academics_results_int_p_subject'
#
#
# class AcademicsResultsIntSubject(ResultsBaseModel):
#     class Meta:
#         db_table = 'academics_results_int_subject'
#
#
# class AcademicsResultsIntOverall(ResultsBaseModel):
#     class Meta:
#         db_table = 'academics_results_int_overall'
