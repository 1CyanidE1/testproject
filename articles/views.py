from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Article, Tag
from .forms import CustomUserCreationForm, ArticleForm


@login_required
def article_list(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(request, 'articles/article_list.html', {'articles': articles})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'articles/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'articles/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@user_passes_test(lambda u: u.is_staff)
def moderation_list(request):
    articles = Article.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'articles/moderation_list.html', {'articles': articles})


@user_passes_test(lambda u: u.is_staff)
def moderate_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'publish':
            article.status = 'published'
            article.rejection_reason = ''
        elif action == 'reject':
            article.status = 'rejected'
            article.rejection_reason = request.POST.get('rejection_reason', '')
        article.save()
        return redirect('moderation_list')
    return render(request, 'articles/moderate_article.html', {'article': article})


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'pending'
            article.save()

            form.save_m2m()

            # new_tags = form.cleaned_data['new_tags']
            # if new_tags:
            #     new_tags_list = [tag.strip() for tag in new_tags.split(',')]
            #     for tag_name in new_tags_list:
            #         tag, created = Tag.objects.get_or_create(name=tag_name)
            #         article.tags.add(tag)

            return redirect('article_list')
        else:
            print(form.errors)
            print(request.POST.getlist('tags'))
    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form})


@login_required
def user_profile(request):
    published_articles = Article.objects.filter(author=request.user, status='published')
    pending_articles = Article.objects.filter(author=request.user, status='pending')
    rejected_articles = Article.objects.filter(author=request.user, status='rejected')
    return render(request, 'articles/user_profile.html', {
        'published_articles': published_articles,
        'pending_articles': pending_articles,
        'rejected_articles': rejected_articles
    })
