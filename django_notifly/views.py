from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserNotification


def notification_click(request, user_notification_id):
    user_notification = UserNotification.objects.get(
        id=user_notification_id, user=request.user
    )
    user_notification.mark_as_read()
    return redirect(user_notification.notification.url)


def read_notification(request, user_notification_id):
    print("notifoaction lue")
    user_notification = UserNotification.objects.get(
        id=user_notification_id, user=request.user
    )
    user_notification.mark_as_read()
    return HttpResponse("")


def unread_count(request):
    count = count = UserNotification.objects.filter(
        user=request.user, is_read=False
    ).count()
    return render(
        request, "django_Notifly/unread_notifications_count.html", {"count": count}
    )


# @login_required
def all_notifications_view(request):
    notifications = UserNotification.objects.filter(user=request.user)
    return render(
        request,
        "django_Notifly/all_notifications.html",
        {"notifications": notifications},
    )
