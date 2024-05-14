from .models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'unread_notifications_count': unread_notifications_count,
            'notifications': notifications
        }
    return {}