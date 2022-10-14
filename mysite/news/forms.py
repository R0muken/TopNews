from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import News, Comment
import re


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets = {
        #     "username": forms.TextInput(attrs={"class": "form-control"}),
        #     "email": forms.EmailInput(attrs={"class": "form-control"}),
        #     "password1": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "password2": forms.PasswordInput(attrs={"class": "form-control"})
        # }


class NewsForm(forms.ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = News
        exclude = ("author",)
        fields = ["title", "content", "photo", "is_published", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Incorrect title: Starts with Number')
        return title

    def clean_is_published(self):
        is_published = self.cleaned_data['is_published']
        if not is_published:
            raise ValidationError('News must be published')
        return is_published


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = True

    class Meta:
        model = Comment
        exclude = ("news", "user")
        fields = ["body",]