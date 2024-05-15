from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django_select2.forms import Select2MultipleWidget, ModelSelect2MultipleWidget

from .models import CustomUser, Article, Tag


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',
    }

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=(
            'Ваш пароль не должен быть слишком похож на другую вашу личную информацию.<br>'
            'Ваш пароль должен содержать не менее 8 символов.<br>'
            'Ваш пароль не может быть часто используемым паролем.<br>'
            'Ваш пароль не может состоять только из цифр.'
        ),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'password1', 'password2')

        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'name': 'Имя',
        }
        help_texts = {
            'username': 'Обязательно. Только буквы, цифры и @/./+/-/_.',
        }
        error_messages = {
            'username': {
                'unique': 'Пользователь с таким именем уже существует.',
            },
            'email': {
                'unique': 'Пользователь с таким адресом электронной почты уже существует.',
                'invalid': 'Введите правильный адрес электронной почты.',
            },
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=254,
        error_messages={
            'required': 'Пожалуйста, введите имя пользователя.',
            'invalid': 'Введите правильное имя пользователя.',
        }
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Пожалуйста, введите пароль.',
            'invalid': 'Введите правильный пароль.',
        }
    )


class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'js-example-basic-multiple'}),
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'text', 'tags']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'tags': 'Теги'
        }


class ModerationForm(forms.Form):
    action = forms.ChoiceField(choices=[('publish', 'Publish'), ('reject', 'Reject')])
    rejection_reason = forms.CharField(widget=forms.Textarea, required=False)


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=ModelSelect2MultipleWidget(
            attrs={'class': 'form-control select2'}
        ),
    )
