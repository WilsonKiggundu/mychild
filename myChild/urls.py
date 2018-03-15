
from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin
from api.resources import *
from api.views import user_login
from front.views import *

school_resource = SchoolResource()
student_resource = StudentResource()
user_resource = UserResource()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='admin'),

    # api
    url(r'^api/', include(school_resource.urls)),
    url(r'^api/', include(student_resource.urls)),
    url(r'^api/', include(user_resource.urls)),
    url(r'^api/docs', include(user_resource.urls)),

    # user login
    url(r'^login/$', auth_login, name='auth-login'),
    url(r'^register/$', user_signup, name='signup'),
    url(r'^logout/$', auth_logout, name='logout'),

    # school
    url(r'^school/register/$', register_school, name='register-school'),
    url(r'^students/$', get_students, name='students'),
    url(r'^student/([0-9]+)/details/$', student_details, name='student_details'),
    url(r'^student/(?P<student_id>[0-9]+)/(?P<year>[0-9]{4})/(?P<term>[0-9])/results/$',
        student_results, name='student_results'),
    url(r'^student/(?P<student_id>[0-9]+)/results/$', student_results, name='student_results'),
    url(r'^calendar/$', calendar, name='calendar'),

    # profile
    url(r'^profile/create/$', create_profile, name='create-profile'),
    url(r'^user/create/$', create_user, name='create-user'),
    url(r'^user/profile/$', user_profile, name='user_profile'),
    url(r'^user/profile/([0-9]+)/$', user_profile, name='user_profile'),
    url(r'^parents/$', get_parents, name='parents'),
    url(r'^profile/add/child/$', add_child, name='add_child'),
    url(r'^profile/add/school/$', add_school, name='add_school'),
    url(r'^schools/$', get_schools, name='get_schools'),

    # messages

    # stream
    url(r'^$', home, name='home'),

    # posts
    url(r'^post/create/$', create_post, name='create-post'),
    url(r'^comment/$', create_comment, name='create_comment'),

    # imports
    url(r'^import/students/$', import_students, name='import_students'),
    url(r'^import/results/$', import_academic_results, name='import_results'),
    url(r'^import/classes/$', import_classes, name='import_classes'),
    url(r'^import/subjects/$', import_subjects, name='import_subjects'),

    # exports
    url(r'^generate/students/template/$', generate_students_list_template, name='students_list_template'),
    url(r'^generate/subjects/template/$', generate_subjects_list_template, name='subjects_list_template'),
    url(r'^generate/results/template/$', generate_results_template, name='results_template'),
    url(r'^generate/classes/template/$', generate_class_list_template, name='class_list_template'),
]
