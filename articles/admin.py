from django.contrib import admin
from .models import CustomUser, Article, Tag

admin.site.register(CustomUser)
admin.site.register(Article)
admin.site.register(Tag)
