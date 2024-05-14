from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_select2.forms import Select2MultipleWidget

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

