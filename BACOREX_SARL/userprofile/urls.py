from django.urls import path

from . import views

urlpatterns = [
    path('',views.connexion, name="connexion"),
    path('logout', views.logout, name='logout')
]