import csv
import pdb

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from api.imports import StudentCsvImportModel, process_csv_file, generate_students_list_template
from api.models import SchoolContactPerson, Post, Attachment, Student, Nok, Profile
from api.utils import generate_student_code
from front.forms import SchoolForm, ProfileForm, UserForm, SchoolContactForm, PostForm, AttachmentForm, ImportForm


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

            lines = process_csv_file(request, True)

            for line in lines:
                line = line.split(',')

                code = generate_student_code()
                admission_number = line[0]
                name = line[1].split(' ')
                first_name = name[0]
                last_name = name[1]
                date_of_birth = line[2]
                gender = line[3]
                school_class = line[4]
                stream = line[5]
                dormitory = line[6]
                religion = line[7]
                district = line[8]
                nationality = line[9]
                home_address = line[10]
                email = line[11]
                date_joined = line[12]
                class_joined = line[13]
                disabled = line[14]
                other_info = line[15]
                student_nin = line[16]
                school_id = 1

                father_name = line[17]
                father_telephone = line[18]
                father_email = line[19]
                father_occupation = line[20]
                father_nin = line[21]

                mother_name = line[22]
                mother_telephone = line[23]
                mother_email = line[24]
                mother_occupation = line[25]
                mother_nin = line[26]

                if category == '1':

                    student = Student(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                                      gender=gender,school_class=school_class, stream=stream, other_info=other_info,
                                      nin=student_nin, admission_number=admission_number, school_id=school_id,
                                      religion=religion, code=code)
                    student.save()

                    print(father_name)

                    ''' add parents '''
                    if father_name:
                        name = father_name.split(' ')
                        user = User(email=father_email, username=father_email, is_active=False, first_name=name[0],
                                    last_name=name[1], )
                        user.save(commit=False)

                        user.set_password('sw33th0m3')
                        # user.save()

                        father = Nok(name=father_name, student=student, occupation=father_occupation, relationship='Father',
                                 nin=father_nin, profile=Profile(user=user, type='Parent', ))

                        father.save()

                    if mother_name:
                        name = mother_name.split(' ')
                        user = User(email=mother_email, username=mother_email, is_active=False, first_name=name[0],
                                    last_name=name[1], )
                        user.save(commit=False)

                        user.set_password('sw33th0m3')
                        # user.save()

                        mother = Nok(name=mother_name, student=student, occupation=mother_occupation,
                                     relationship='Mother',
                                     nin=mother_nin, profile=Profile(user=user, type='Parent', ))

                        mother.save()

            return HttpResponseRedirect(reverse('thanks'))

    return render(request, 'admin/import.html', {
        'model': {
            'form': form,
            'action': 'import-data'
        }
    })


def get_template(request):
    return generate_students_list_template(request, 'CSV')