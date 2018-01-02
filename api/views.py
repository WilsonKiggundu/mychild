import coreapi
from django.contrib.auth import authenticate
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods


def get_students(request):
    client = coreapi.Client()
    students = client.get('/api/student/')


@require_http_methods(["POST"])
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user:
        return JsonResponse({'id': user})

    return JsonResponse({'message': 'Invalid username/password'})