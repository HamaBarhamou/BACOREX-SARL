from django.shortcuts import render
from django.shortcuts import redirect
from .models import UserNotification



def notification_click(request, user_notification_id):
    user_notification = UserNotification.objects.get(id=user_notification_id, user=request.user)
    user_notification.mark_as_read()
    return redirect(user_notification.notification.url)


def unread_count(request):
    count = count = UserNotification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'django_Notifly/unread_notifications_count.html', {'count': count})