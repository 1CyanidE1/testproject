from .models import Notification


def send_notification(user, article, message):
    Notification.objects.create(
        user=user,
        article=article,
        message=message
    )