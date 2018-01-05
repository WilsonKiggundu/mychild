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


'''Profile'''
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

''' School '''
admin.site.register(School)
admin.site.register(SchoolClass)
admin.site.register(SchoolCommunication)
admin.site.register(SchoolEvent)
admin.site.register(Subject)
admin.site.register(SubjectGroup)
admin.site.register(SubjectPaper)

''' Student '''
admin.site.register(Student)
