from django.urls import path

from . import views

urlpatterns = [
    path('',views.magasin_home, name='magasin_home'),
    path('categorie',views.categorie_home, name='categorie'),
]