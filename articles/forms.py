from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_select2.forms import Select2MultipleWidget, ModelSelect2MultipleWidget

from .models import CustomUser, Article, Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'password1', 'password2')


class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'select2'}),
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'text', 'tags']


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
