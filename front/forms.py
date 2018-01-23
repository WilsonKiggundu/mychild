from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelChoiceField

from api.models import School, Profile, SchoolContactPerson, SchoolClass, Subject
from api.options import VIEWERS, IMPORTS, YEARS, TERMS, CURRICULUM_LEVELS, RESULTS_CATEGORIES
from front.fields import SubjectModelChoiceField


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('status', 'vision', 'mission', 'psm_id',)


class SchoolContactForm(forms.ModelForm):
    class Meta:
        model = SchoolContactPerson
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput)
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, label='Remember me', widget=forms.CheckboxInput)


class SignupForm(forms.Form):
    child_code = forms.CharField(required=True, label='My Child Code')
    school_code = forms.CharField(required=True, label='School Code')
    first_name = forms.CharField(required=True, label='First name')
    last_name = forms.CharField(required=True, label='Last name')
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords don''t match')


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('type', 'school', 'user', 'telephone', 'bio')


class AttachmentForm(forms.Form):
    files = forms.FileField(label='Choose files to upload', widget=forms.ClearableFileInput(attrs={'multiple': True, }))


class NewsFeedForm(forms.Form):
    details = forms.CharField(max_length=20000, widget=forms.Textarea(attrs={'class':'form-control'}))
    files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, }))


class CommentForm(forms.Form):
    author = forms.IntegerField()
    details = forms.Textarea()


class ImportForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all())
    category = forms.CharField(required=True, widget=forms.Select(choices=IMPORTS))
    file = forms.FileField(required=True)


class GenerateResultsTemplateForm(forms.Form):
    category = forms.CharField(required=True, widget=forms.Select(choices=RESULTS_CATEGORIES))
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all(), to_field_name='id')
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), to_field_name='id')
    year = forms.CharField(required=True, widget=forms.Select(choices=YEARS))
    term = forms.CharField(required=True, widget=forms.Select(choices=TERMS))


class ImportStudentsForm(forms.Form):
    files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, }))


class ImportClassesForm(forms.Form):
    file = forms.FileField(required=True)


class ImportSubjectsForm(forms.Form):
    file = forms.FileField(required=True)


class ImportResultsForm(forms.Form):
    files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, }))


class AddChildForm(forms.Form):
    child_code = forms.CharField(required=True)
    school_code = forms.CharField(required=True)