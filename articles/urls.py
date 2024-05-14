from django.urls import path
from .views import article_list, register, login_view, logout_view, moderation_list, moderate_article, create_article, \
    user_profile, article_detail

urlpatterns = [
    path('', article_list, name='article_list'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('moderation/', moderation_list, name='moderation_list'),
    path('moderate/<int:article_id>/', moderate_article, name='moderate_article'),
    # path('approve/<int:article_id>/', approve_article, name='approve_article'),
    # path('reject/<int:article_id>/', reject_article, name='reject_article'),
    path('create/', create_article, name='create_article'),
    path('profile/', user_profile, name='user_profile'),
]
