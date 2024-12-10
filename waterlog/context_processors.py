from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            wprofile__waterUser=request.user,
            read=False
        ).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
