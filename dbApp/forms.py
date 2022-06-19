from django import forms
from .models import Question, Answer, Profile, Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField()


class QuestionForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()
