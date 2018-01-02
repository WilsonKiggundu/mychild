from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from api.models import School, Profile, SchoolContactPerson
from api.options import VIEWERS, IMPORTS


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('status', 'vision', 'mission', 'psm_id',)


class SchoolContactForm(forms.ModelForm):
    class Meta:
        model = SchoolContactPerson
        fields = '__all__'


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


class PostForm(forms.Form):
    author = forms.IntegerField(widget=forms.HiddenInput)
    title = forms.CharField(required=False, max_length=255)
    details = forms.CharField(max_length=2000, widget=forms.Textarea())
    files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, }))
    viewers = forms.MultipleChoiceField(required=False, choices=VIEWERS, widget=forms.CheckboxSelectMultiple(attrs={'class': 'inline'}))


class CommentForm(forms.Form):
    author = forms.IntegerField()
    details = forms.Textarea()


class ImportForm(forms.Form):
    category = forms.CharField(required=True, widget=forms.Select(choices=IMPORTS))
    file = forms.FileField(required=True)