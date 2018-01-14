from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('first_name', 'last_name', 'email', 'type', 'school')

    def school(self, obj):
        return obj.profile.school

    def type(self, obj):
        return obj.profile.type




'''Profile'''
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

''' School '''
admin.site.register(School)


class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream', 'class_teacher', 'curriculum', 'level', 'school')
    list_filter = ('school', 'curriculum', 'level')


admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(SchoolCommunication)
admin.site.register(SchoolEvent)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'code', 'level', 'curriculum', 'standard', 'school', 'remarks')
    list_filter = ('school', 'level', 'curriculum', 'standard')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectGroup)
admin.site.register(SubjectPaper)

''' Results '''


class ALevelOverallAdmin(admin.ModelAdmin):
    list_filter = ()


admin.site.register(AcademicsResultsLocalALevelOverall, ALevelOverallAdmin)
admin.site.register(AcademicsResultsLocalALevelSubject)
admin.site.register(AcademicsResultsLocalOLevelOverall)
admin.site.register(AcademicsResultsLocalOLevelSubject)
admin.site.register(AcademicsResultsLocalPrimaryOverall)
admin.site.register(AcademicsResultsLocalPrimarySubject)


class PaperResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'mark', 'grade', 'school_class', 'stream', 'term', 'year',
                    'stream_position', 'class_position', 'comment', 'school')
    list_filter = ('subject', 'school_class', 'stream', 'term', 'year', 'school')


admin.site.register(AcademicsResultsMarks, PaperResultsAdmin)

''' Student '''


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'admission_number', 'school_class', 'stream', 'code', 'school')
    list_filter = (
        'school',
        'gender',
        'school_class',
        'stream',
    )


admin.site.register(Student, StudentAdmin)


class AttachmentsInline(admin.StackedInline):
    model = Attachment
    extra = 0


class NewsFeedAdmin(admin.ModelAdmin):
    list_display = ('details', 'author', 'parent', 'date', 'school',)
    inlines = [AttachmentsInline]


admin.site.register(NewsFeed, NewsFeedAdmin)



