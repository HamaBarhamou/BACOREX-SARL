from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dao, name='home_dao'),
    path('add/', views.add_dao, name='add_dao')
]
