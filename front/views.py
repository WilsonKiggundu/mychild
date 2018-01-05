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


def import_data(request):
    form = ImportForm()

    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)

        if form.is_valid():
            category = form.cleaned_data['category']
            school_id = form.cleaned_data['school']

            lines = process_csv_file(request, True)

            for line in lines:
                line = line.split(',')

                if category == '1':

                    code = generate_student_code()

                    name = line[0].split(' ')
                    first_name = name[0]
                    last_name = name[1]

                    admission_number = line[1]
                    school_class = line[2]
                    stream = line[3]
                    gender = line[4]
                    nationality = line[5]
                    other_info = line[6]
                    student_nin = line[7]

                    father_name = line[8]
                    father_telephone = line[9]
                    father_email = line[10]
                    father_occupation = line[11]
                    father_nin = line[12]

                    mother_name = line[13]
                    mother_telephone = line[14]
                    mother_email = line[15]
                    mother_occupation = line[16]
                    mother_nin = line[17]

                    student = Student(first_name=first_name, last_name=last_name,
                                      gender=gender, school_class=school_class, stream=stream, other_info=other_info,
                                      nin=student_nin, admission_number=admission_number, school_id=school_id,
                                      code=code)
                    student.save()

                    ''' add parents '''
                    if father_name:
                        name = father_name.split(' ')
                        user = User(email=father_email, username=father_email, is_active=False, first_name=name[0],
                                    last_name=name[1], )
                        # user.save(commit=False)

                        user.set_password('sw33th0m3')
                        user.save()

                        profile = Profile(user=user, type='Parent', )
                        profile.save()

                        father = Nok(name=father_name, student=student, occupation=father_occupation,
                                     relationship='Father',
                                     nin=father_nin, profile=profile)

                        father.save()

                    if mother_name:
                        name = mother_name.split(' ')
                        user = User(email=mother_email, username=mother_email, is_active=False, first_name=name[0],
                                    last_name=name[1], )
                        # user.save(commit=False)

                        user.set_password('sw33th0m3')
                        user.save()

                        profile = Profile(user=user, type='Parent', )
                        profile.save()

                        mother = Nok(name=mother_name, student=student, occupation=mother_occupation,
                                     relationship='Mother',
                                     nin=mother_nin, profile=profile)

                        mother.save()

                elif category == '5':  # Import classes
                    name = line[0]
                    class_number = line[1]
                    stream = line[2]
                    level_short = line[3]
                    curriculum = line[4]
                    progression = line[5]

                    school_class = SchoolClass(name=name, stream=stream, level_short=level_short,
                                               progression=progression, class_number=class_number,
                                               curriculum=curriculum, school_id=school_id)

                    school_class.save()

            return HttpResponseRedirect(reverse('thanks'))

    return render(request, 'admin/import.html', {
        'model': {
            'form': form,
            'action': 'import-data'
        }
    })


def generate_template(request):
    form = ImportResultsForm()

    if request.method == 'POST':
        form = ImportResultsForm(request.POST)
        if form.is_valid():
            return generate_academic_results_template(request)

    return render(request, 'form.html', {
        'model': {
            'form': form,
            'action': 'export-data'
        }
    })


def get_template(request, category='1'):
    if category == '1':
        return generate_students_list_template(request, 'CSV')
    if category == '5':
        return generate_class_list_template(request, 'CSV')
