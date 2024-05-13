from django.urls import path
from .views import article_list, register, login_view, logout_view, moderation_list, moderate_article, create_article, \
    user_profile

urlpatterns = [
    path('', article_list, name='article_list'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('moderation/', moderation_list, name='moderation_list'),
    path('moderate/<int:article_id>/', moderate_article, name='moderate_article'),
    path('create/', create_article, name='create_article'),
    path('profile/', user_profile, name='user_profile'),
]
