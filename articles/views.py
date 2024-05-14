from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

from .models import Article, Tag
from .forms import CustomUserCreationForm, ArticleForm, ModerationForm, SearchForm


def article_list(request):
    form = SearchForm(request.GET)
    articles = Article.objects.filter(status='published').order_by('-created_at')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        tags = form.cleaned_data.get('tags')

        if query:
            articles = articles.filter(title__icontains=query)

        if tags:
            articles = articles.filter(tags__in=tags).distinct()

    return render(request, 'articles/article_list.html', {'articles': articles, 'form': form})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/article_detail.html', {'article': article})


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


def is_moderator(user):
    return user.is_staff


@login_required
@user_passes_test(lambda u: u.is_staff)
def moderate_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = ModerationForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            if action == 'publish':
                article.status = 'published'
                article.rejection_reason = ''
            elif action == 'reject':
                article.status = 'rejected'
                article.rejection_reason = form.cleaned_data['rejection_reason']
            article.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ModerationForm()

    return render(request, 'articles/moderate_article.html', {'form': form, 'article': article})


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'pending'
            article.save()

            # Обработка тегов
            tags = form.cleaned_data['tags']
            for tag in tags:
                tag.usage_count += 1
                tag.save()
            form.save_m2m()

            return redirect('article_list')
        else:
            print(form.errors)
            print(request.POST.getlist('tags'))
            print(Tag.objects.filter(id__in=request.POST.getlist('tags')))
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


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.status = 'pending'
            article.save()
            form.save_m2m()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return HttpResponseForbidden()
