from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Book.models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'type', 'text', 'image', 'private_choise']
        labels = {'title': '', 'type': 'Тип', 'text': '', 'image': 'Выберите изображение', 'private_choise': ''}
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Название'}),
            'text': Textarea(attrs={'placeholder': 'Описание'}),
        }
        

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'}))    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите адрес эл. почты'}))   
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'}))   
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
            