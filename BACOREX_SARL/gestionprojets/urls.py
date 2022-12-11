from django.urls import path

from . import views

urlpatterns = [
    path('', views.listeProject, name = 'listeproject'),
    path('listeclient', views.listeClient, name = 'listeclient'),
    path('newclient', views.newClient, name = 'newclient')
]