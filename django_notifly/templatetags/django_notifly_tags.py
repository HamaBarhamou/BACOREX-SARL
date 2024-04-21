from django import template
from django_notifly.models import Notification, UserNotification
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.urls import reverse
from django.core.paginator import Paginator

register = template.Library()


""" @register.inclusion_tag("django_Notifly/all_notifications.html", takes_context=True)
def render_notifications(context):
    request = context["request"]
    notifications = UserNotification.objects.filter(user=request.user)
    return {"notifications": notifications} """


@register.inclusion_tag(
    "django_Notifly/notifications_dropdown.html", takes_context=True
)
def user_notifications(context):
    user = context["request"].user
    notifications = UserNotification.objects.filter(
        user=user, is_read=False
    ).select_related("notification")
    return {"user_notifications": notifications}


@register.simple_tag(takes_context=True)
def unread_notifications_count(context):
    request = context["request"]
    if request.user.is_authenticated:
        unread_count = UserNotification.objects.filter(
            user=request.user, is_read=False
        ).count()
        # Rendre le template avec le contexte nécessaire
        return render_to_string(
            "django_Notifly/unread_notifications_count.html",
            {
                "unread_count": unread_count,
                "user": request.user,
            },
        )
    return ""


@register.inclusion_tag("django_Notifly/all_notifications.html", takes_context=True)
def all_notifications(context):
    request = context["request"]
    notifications = UserNotification.objects.filter(user=request.user)
    return {"notifications": notifications}
