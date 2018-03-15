from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from tastypie.authentication import MultiAuthentication, BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.http import HttpForbidden, HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from api.models import *


class SchoolResource(ModelResource):
    class Meta:
        queryset = School.objects.all()
        resource_name = 'school'
        authorization = Authorization()


class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'student'
        authorization = Authorization()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/login'
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        authorization = Authorization()

        # authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())

    def prepend_urls(self):
        return [
            url(r"^user/login/$", self.wrap_view('login'), name="api_login"),
            url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect username/password',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)
