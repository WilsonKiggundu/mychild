from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)
    list_display = ('first_name', 'last_name', 'email', 'type', 'school')
    list_filter = ('profile__school', 'profile__type')
    search_fields = ('first_name', 'last_name', 'email',)

    def school(self, obj):
        return obj.profile.school

    def type(self, obj):
        return obj.profile.type


'''Profile'''
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

''' School '''


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'email_address', 'telephone', 'physical_address', 'local_curriculum',
                    'international_curriculum',
                    'pre_primary_curriculum')
    list_filter = ('local_curriculum', 'international_curriculum', 'pre_primary_curriculum')


admin.site.register(School, SchoolAdmin)


class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream', 'class_teacher', 'curriculum', 'level', 'school')
    list_filter = ('school', 'curriculum', 'level')


admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(SchoolCommunication)
admin.site.register(SchoolEvent)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'code', 'level', 'curriculum', 'standard', 'school', )
    list_filter = ('school', 'level', 'curriculum', 'standard')
    search_fields = ['name', 'short', 'standard']
    list_per_page = 15


admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectGroup)
admin.site.register(SubjectPaper)

''' Results '''


class ALevelOverallAdmin(admin.ModelAdmin):
    list_filter = ()


class OLevelOverallAdmin(admin.ModelAdmin):
    list_display = ('student', 'school', 'term', 'year', 'school_class', 'aggregate',
                    'class_position', 'stream_position', 'total_marks', 'average_mark',
                    'class_teacher_comment', 'house_teacher_comment', 'head_teacher_comment')
    list_filter = ('school', 'term', 'year', 'school_class')
    search_fields = ['student__first_name', 'student__last_name']


admin.site.register(AcademicsResultsLocalALevelOverall, ALevelOverallAdmin)
admin.site.register(AcademicsResultsLocalALevelSubject)
admin.site.register(AcademicsResultsLocalOLevelOverall, OLevelOverallAdmin)


class OLevelSubjectResultsAdmin(admin.ModelAdmin):
    list_display = ('student','school_class', 'subject', 'mark', 'grade', 'term', 'year')
    list_filter = ('school', 'term', 'year', 'school_class')
    search_fields = ['student__first_name', 'student__last_name', 'subject__name']


admin.site.register(AcademicsResultsLocalOLevelSubject, OLevelSubjectResultsAdmin)
admin.site.register(AcademicsResultsLocalPrimaryOverall)
admin.site.register(AcademicsResultsLocalPrimarySubject)


class PaperResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'mark', 'grade', 'school_class', 'term', 'year',
                    'stream_position', 'class_position', 'comment', 'school')
    list_filter = ('subject', 'school_class', 'term', 'year', 'school')


admin.site.register(AcademicsResultsMarks, PaperResultsAdmin)

''' Student '''


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'admission_number',
                    'school_class', 'code', 'school')
    list_filter = (
        'school',
        'gender',
        'school_class',
    )
    search_fields = ['first_name', 'last_name', 'admission_number']


admin.site.register(Student, StudentAdmin)


class AttachmentsInline(admin.StackedInline):
    model = Attachment
    extra = 0


class CommentsInline(admin.StackedInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = (CommentsInline,)
    list_display = ('id', 'details', 'author', 'date')
    list_display_links = ('id', 'details')


admin.site.register(Post, PostAdmin)
