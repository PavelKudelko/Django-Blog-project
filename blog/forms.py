from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       UserChangeForm)
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import Comment, Article, Category


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    # is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'last_login',
                  'date_joined',
                  )


class ArticleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Your title"
    }))
    content = forms.Textarea()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")
    snippet = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your snippet"}))

    class Meta:
        model = Article
        fields = [
            'title',
            'snippet',
            'content',
            'category',
        ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )
