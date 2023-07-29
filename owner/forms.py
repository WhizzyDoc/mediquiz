from django import forms
from django.contrib.auth.models import User
from quiz.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('f_name', 'l_name', 'photo', 'about', 'school', 'course', 'quiz')

