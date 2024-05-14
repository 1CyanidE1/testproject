from django.urls import path
from .views import article_list, register, login_view, logout_view, moderation_list, moderate_article, create_article, \
    user_profile, article_detail, edit_article, delete_article, notification_list, mark_as_read

urlpatterns = [
    path('', article_list, name='article_list'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('edit/<int:article_id>/', edit_article, name='edit_article'),
    path('delete/<int:article_id>/', delete_article, name='delete_article'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('moderation/', moderation_list, name='moderation_list'),
    path('moderate/<int:article_id>/', moderate_article, name='moderate_article'),
    path('create/', create_article, name='create_article'),
    path('profile/', user_profile, name='user_profile'),
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
]
