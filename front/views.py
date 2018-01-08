from actstream.models import Action, user_stream
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.views.decorators.http import require_http_methods

from api.imports import *
from api.models import *
from api.utils import generate_student_code
from front.forms import *


# Create your views here.

def auth_login(request):
    form = LoginForm()
    messages = []

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)

            if user:
                return HttpResponseRedirect(reverse('home'))
            messages.append("Invalid email and/or password")

    return render(request, 'form.html', {
        'model': {
            'form': form,
            'action': 'auth-login',
            'messages': messages
        }
    })


def user_signup(request):
    form = SignupForm()
    messages = []

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

    return render(request, 'form.html', {
        'model': {
            'form': form,
            'action': 'signup',
            'messages': messages
        }
    })


def get_stream(request):
    stream = user_stream(request.user, with_user_activity=True)
    return render(request, 'stream.html', {'stream': stream})


def home(request):
    return render(request, 'home.html')


def create_user(request):
    form = UserForm()
    messages = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.is_active = True

        if form.is_valid():
            user = form.save(commit=True)

            if user:

                ''' log the user in '''
                username = request.POST['username']
                password = request.POST['password']

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    return HttpResponseRedirect(reverse('register-school'))

    return render(request, 'user/create.html', {
        'model': {
            'form': form,
            'action': 'create-user',
        }
    })


@require_http_methods(['GET', 'POST'])
def register_school(request):
    form = SchoolForm()
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            if school:
                user = request.user.id

                return render(request, 'profile/create.html', {
                    'model': {
                        'form': ProfileForm({'school': school.pk, 'user': user, 'type': 'Teacher'}),
                        'action': 'create-profile',
                    }
                })

    return render(request, 'school/register.html', {
        'model': {
            'form': form,
            'action': 'register-school'
        }
    })


@require_http_methods(["POST"])
@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save()

            if profile:
                person = SchoolContactPerson(profile=profile, school=profile.school)
                person.save()

                return HttpResponseRedirect('/thanks/')

        else:
            return render(request, 'profile/create.html', {
                'model': {
                    'form': form,
                    'action': 'create-profile',
                }
            })


def thanks(request):
    # logout(request)
    return render(request, 'thanks.html')


''' User posts '''


@require_http_methods(["GET", "POST"])
def create_post(request):
    form = PostForm({'author': request.user.id})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        title = request.POST['title']
        details = request.POST['details']
        viewers = request.POST['viewers']

        if form.is_valid():
            post = Post(author=request.user, type='Blog', title=title, details=details, viewers=viewers)

            try:
                post.save()

                ''' upload the files '''
                files = request.FILES.getlist('files')
                if files is not None:
                    for file in files:
                        attachment = Attachment(file=file, post=post, content_type=file.content_type)
                        attachment.save()

                return HttpResponseRedirect(reverse('thanks'))
            except():
                pass

    return render(request, 'posts/create.html', {
        'model': {
            'form': form,
            'action': 'create-post'
        }
    })


def import_academic_results(request):
    form = ImportResultsForm()
    if request.method == 'POST':
        form = ImportResultsForm(request.POST, request.FILES)

        if form.is_valid():
            process_excel_file(request, Imports.students)
            return HttpResponseRedirect(reverse('thanks'))

    return render(request, 'admin/import.html', {
        'model': {
            'form': form,
            'action': 'import_academic_results'
        }
    })


def import_students(request):
    form = ImportStudentsForm()

    if request.method == "POST":
        form = ImportStudentsForm(request.POST, request.FILES)

        if form.is_valid():
            process_excel_file(request, Imports.students)
            return HttpResponseRedirect(reverse('thanks'))

    return render(request, 'admin/import.html', {
        'model': {
            'form': form,
            'action': 'import-data'
        }
    })


def import_classes(request):
    form = ImportClassesForm()

    if request.method == "POST":
        form = ImportClassesForm(request.POST, request.FILES)

        if form.is_valid():
            process_excel_file(request, Imports.classes)
            return HttpResponseRedirect(reverse('thanks'))

    return render(request, 'admin/import.html', {
        'model': {
            'form': form,
            'action': 'import_classes'
        }
    })


def import_subjects(request):
    form = ImportSubjectsForm()

    if request.method == "POST":
        form = ImportSubjectsForm(request.POST, request.FILES)

        if form.is_valid():
            process_excel_file(request, Imports.subjects)
            return HttpResponseRedirect(reverse('thanks'))

    return render(request, 'admin/import.html', {
        'model': {
            'form': form,
            'action': 'import_subjects'
        }
    })


def generate_template(request):
    form = GenerateResultsTemplateForm()

    if request.method == 'POST':
        form = GenerateResultsTemplateForm(request.POST)
        if form.is_valid():
            return generate_academic_results_template(request)

    return render(request, 'form.html', {
        'model': {
            'form': form,
            'action': 'export-data'
        }
    })


def get_students_list_template(request):
    return generate_students_list_template(request)
