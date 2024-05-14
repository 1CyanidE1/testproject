from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Article, Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'password1', 'password2')


class ArticleForm(forms.ModelForm):
    new_tags = forms.CharField(max_length=255, required=False, help_text="Enter new tags separated by commas")

    class Meta:
        model = Article
        fields = ['title', 'text', 'new_tags']
        # widgets = {
        #     'tags': forms.SelectMultiple,
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['tags'].queryset = Tag.objects.all().order_by('-usage_count')[:10]

    def save(self, commit=True):
        article = super().save(commit=False)
        new_tags = self.cleaned_data.get('new_tags', '')
        if commit:
            article.save()
            self.save_m2m()
            if new_tags:
                new_tags_list = [tag.strip() for tag in new_tags.split(',')]
                for tag_name in new_tags_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    article.tags.add(tag)
        return article
