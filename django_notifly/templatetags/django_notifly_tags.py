from django import template
from django_notifly.models import Notification

register = template.Library()


@register.inclusion_tag("django_Notifly/all_notifications.html", takes_context=True)
def render_notifications(context):
    request = context["request"]
    # notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    return {"notifications": "notifications"}
