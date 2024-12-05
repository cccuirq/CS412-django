# waterlog/context_processors.py
from .models import Notification, WProfile
from django.shortcuts import get_object_or_404

def unread_notifications_count(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(WProfile, waterUser=request.user)
        unread_count = Notification.objects.filter(wprofile=user_profile, read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
