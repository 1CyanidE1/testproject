from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_stuff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)  # TODO; Сделать обязательным
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def add_tag(self, tag_name):
        tag, created = Tag.objects.get_or_create(name=tag_name)
        self.tags.add(tag)

    def remove_tag(self, tag_name):
        try:
            tag = Tag.objects.get(name=tag_name)
            self.tags.remove(tag)
        except Tag.DoesNotExist:
            pass


@receiver(m2m_changed, sender=Article.tags.through)
def update_tag_usage_count(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
        for tag in instance.tags.all():
            tag.usage_count = tag.articles.count()
            tag.save()


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.message}'