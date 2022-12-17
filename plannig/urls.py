from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('/<str:date>/<str:cmd>/', views.calendar, name='calendar_post'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
