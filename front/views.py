from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Trunc
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.urls import reverse
from django.views.decorators.http import require_http_methods

from api.imports import *
from api.models import *
from api.utils import generate_student_code
from front.forms import *


# Create your views here.

def auth_login(request):
    message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)

            if user:
                # check if the user school is validated if the trial period has expired
                school = user.profile.school
                validated = school.validated
                reg_date = school.registration_date

                if not validated:
                    message = "You are unable to login because the trial period for your school has expired."
                else:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
            else:
                message = "Invalid email and/or password"
        else:
            message = 'Both email and password are required'

    return render(request, 'user/login.html', {
        'message': message
    })


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth-login'))


def user_signup(request):
    form = SignupForm()
    messages = []

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            child_code = request.POST['child_code']
            school_code = request.POST['school_code']

            try:
                # First check if the school_code and student_code are valid
                student = Student.objects.filter(code__exact=child_code, school_id__exact=school_code).first()
                if student is None:
                    messages.append("Unable to register. Either the child code or school code is invalid")
                else:
                    # Then create a user account
                    user = User(first_name=first_name,
                                last_name=last_name, username=email,
                                email=email, is_active=True)

                    user.set_password(raw_password=password)
                    user.save()

                    # Then create a profile
                    profile = Profile(user=user, school_id=school_code, ).save()

                    # Attach profile student to profile
                    StudentNok(student=student, profile=profile).save()

                    # Then add user as student NOK
                    nok = Nok(student_id=child_code, profile=profile, school_id=school_code)

                    # The sign the user in
                    authenticated = authenticate(request, username=email, password=password)
                    if authenticated:
                        login(request, user)
                        return HttpResponseRedirect(reverse('home'))

            except():
                messages.append("Unable to complete registration at this time")



        else:
            for error in form.errors:
                messages.append(error)

    return render(request, 'user/register.html', {'messages': messages})


@login_required
def home(request):
    posts = Post.objects.order_by('-date')

    return render(request, 'home.html', {'posts': posts})


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
    messages = []
    status_code = 500

    if request.method == 'POST':
        school_name = request.POST['school_name']
        email_address = request.POST['email_address']
        telephone = request.POST['telephone']
        physical_address = request.POST['physical_address']
        contact_first_name = request.POST['contact_first_name']
        contact_last_name = request.POST['contact_last_name']
        contact_telephone = request.POST['contact_telephone']
        contact_role = request.POST['contact_role']
        contact_email_address = request.POST['contact_email_address']
        password = request.POST['password']

        local_curriculum = False
        international_curriculum = False
        curricula = request.POST.getlist('checks[]')

        # return JsonResponse({'messages': messages, 'status_code': 200})

        if '1' in curricula:
            local_curriculum = True
        if '2' in curricula:
            international_curriculum = True

        try:

            # create the user
            user = User(first_name=contact_first_name, last_name=contact_last_name, email=contact_email_address,
                        username=contact_email_address, is_active=True, )
            user.set_password(raw_password=password)
            user.save()

            if user is not None:

                # create the school
                school = School(school_name=school_name, email_address=email_address, telephone=telephone,
                                physical_address=physical_address, status='ACTIVE', validated=False,
                                local_curriculum=local_curriculum, international_curriculum=international_curriculum,)

                school.save()

                if school is not None:

                    # Create user profile
                    profile = Profile(school=school, user=user, type='Teacher', telephone=contact_telephone)
                    profile.save()

                    if profile is not None:

                        contact = SchoolContactPerson(profile=profile, school=school, role=contact_role)
                        contact.save()

                        if contact is not None:

                            status_code = 200
                            messages.append('success')

                            login(request, user)

        except Exception as e:
            messages.append(str(e))

        except IntegrityError as error:
            messages.append(str(error))

        return JsonResponse({'messages': messages, 'status_code': status_code})

    return render(request, 'school/register.html')


@login_required
def get_students(request):
    students = Student.objects.filter(school_id__exact=request.user.profile.school_id)
    return render(request, 'students/index.html', {'students': students})


@login_required
def student_details(request, student_id):
    student = Student.objects.filter(pk=student_id, ).first()
    return render(request, 'students/details.html', {'student': student, })


@login_required
def student_results(request, student_id, year=None, term=None):
    global query
    global overall
    student = Student.objects.filter(pk=student_id, ).first()

    if student.school_class.level_short == 'P':
        query = AcademicsResultsMarks
        overall = AcademicsResultsLocalPrimaryOverall

    elif student.school_class.level_short == 'O':
        query = AcademicsResultsLocalOLevelSubject
        overall = AcademicsResultsLocalOLevelOverall

    elif student.school_class.level_short == 'A':
        query = AcademicsResultsLocalALevelSubject
        overall = AcademicsResultsLocalALevelOverall

    query = query.objects.filter(student_id=student_id).order_by('-year', 'term', 'subject')
    period = query.values('year', 'term').all()

    if year is None:
        year = period[0]['year']
    if term is None:
        term = period[0]['term']

    subject_results = query.filter(year__exact=year, term__exact=term).all()
    overall_results = overall.objects.filter(student_id=student_id, year__exact=year, term__exact=term).first()

    return render(request, 'students/results.html', {
        'student': student,
        'year': year,
        'term': term,
        'periods': list(period),
        'subject_results': subject_results,
        'overall_results': overall_results
    })


@login_required
def get_parents(request):
    parents = Nok.objects.filter(school_id__exact=request.user.profile.school_id, )
    return render(request, 'parents/index.html', {'parents': parents})


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


@login_required
def user_profile(request, profile_id=None):
    user = request.user
    children = None
    if profile_id is not None:
        user = User.objects.filter(profile__id__exact=profile_id).first()
    else:
        children = StudentNok.objects.filter(profile__id__exact=request.user.profile.id)

    return render(request, 'user/profile.html', {
        'user': user,
        'children': children
    })


@login_required
@require_http_methods(['POST'])
def add_child(request):
    messages = []
    form = AddChildForm(request.POST)

    if form.is_valid():
        child_code = request.POST['child_code']
        school_code = request.POST['school_code']
        student = Student.objects.filter(code=child_code, school_id=school_code).first()
        if student:
            StudentNok(student=student, profile=request.user.profile, school=request.user.profile.school).save()
            return HttpResponseRedirect(reverse('user_profile'))
        else:
            messages.append("Invalid student code or school code")

    for error in form.errors:
        messages.append(error)

    children = StudentNok.objects.filter(profile__id__exact=request.user.profile.id)
    return render(request, 'user/profile.html', {
        'user': request.user,
        'children': children,
        'messages': messages
    })


''' User posts '''


@login_required
@require_http_methods(["GET", "POST"])
def create_post(request):
    form = NewsFeedForm()

    if request.method == 'POST':
        form = NewsFeedForm(request.POST, request.FILES)

        details = request.POST['details']

        if form.is_valid():
            post = Post(
                author_id=request.user.id,
                details=details,
                school_id=request.user.profile.school_id,
            )

            try:
                post.save()

                ''' upload the files '''
                files = request.FILES.getlist('files')
                if files is not None:
                    for file in files:
                        attachment = Attachment(file=file, post=post, content_type=file.content_type)
                        attachment.save()

                return HttpResponseRedirect(reverse('home'))

            except():
                pass

    return render(request, 'posts/create.html', {
        'model': {
            'form': form,
            'action': 'create-post'
        }
    })


@require_http_methods(['POST'])
def create_comment(request):
    post_id = request.POST['post_id']
    comment = request.POST['comment']
    author = request.user

    if post_id is not None and comment is not None:
        Comment(post_id=post_id, comment=comment, author=author).save()
        return HttpResponseRedirect(reverse('home'))


def calendar(request):
    return render(request, 'school/calendar.html', {})


# =================
# Imports
# =================


@login_required
def import_academic_results(request):
    message = None
    if request.method == 'POST':
        try:
            process_excel_file(request, Imports.results)
            message = "Results have been imported successfully"
        except():
            message = 'An error occurred while uploading the file'

    return JsonResponse({'message': message})


@login_required
def import_students(request):
    message = None
    if request.method == 'POST':
        try:
            process_excel_file(request, Imports.students)
            message = "Students have been imported successfully"
        except():
            message = 'An error occurred while uploading the file'

    return JsonResponse({'message': message})


@login_required
def import_classes(request):
    message = None
    if request.method == 'POST':
        try:
            process_excel_file(request, Imports.classes)
            message = "Classes have been imported successfully"
        except():
            message = 'An error occurred while uploading the file'

    return JsonResponse({'message': message})


@login_required
def import_subjects(request):
    message = None
    if request.method == 'POST':
        try:
            process_excel_file(request, Imports.subjects)
            message = "Subjects have been imported successfully"
        except():
            message = 'An error occurred while uploading the file'

    return JsonResponse({'message': message})


@login_required
def generate_results_template(request):
    response = []
    if request.method == 'POST':
        try:
            return generate_academic_results_template(request)
        except():
            response.append({'success': 'false'})
            response.append({'message': 'An error occurred while generating the template'})

    return JsonResponse({'response': response})
