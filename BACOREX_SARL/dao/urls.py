from django.urls import path

from . import views

urlpatterns = [
    path('',views.home_dao, name='home_dao')
]