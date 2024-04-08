# django_Notifly/urls.py
from django.urls import path
from .views import unread_count

app_name = 'notifly'

urlpatterns = [
    path('unread-count/', unread_count, name='unread_count'),
]
