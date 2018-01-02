"""myChild URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api.resources import *
from api.views import user_login
from front.views import *

school_resource = SchoolResource()
student_resource = StudentResource()
profile_resource = ProfileResource()
user_resource = UserResource()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # api
    url(r'^api/', include(school_resource.urls)),
    url(r'^api/', include(student_resource.urls)),
    url(r'^api/', include(profile_resource.urls)),
    url(r'^api/', include(user_resource.urls)),
    url(r'^api/docs', include(user_resource.urls)),

    url(r'^$', home, name='home'),
    url(r'^home/$', home, name='home'),

    # school
    url(r'^school/register/$', register_school, name='register-school'),

    # profile
    url(r'^profile/create/$', create_profile, name='create-profile'),
    url(r'^user/create/$', create_user, name='create-user'),

    # messages
    url(r'^thanks/$', thanks, name='thanks'),

    # posts
    url(r'^post/create/$', create_post, name='create-post'),

    # imports
    url(r'^import/$', import_data, name='import-data'),
    url(r'^template/$', get_template, name='get-template'),
]
