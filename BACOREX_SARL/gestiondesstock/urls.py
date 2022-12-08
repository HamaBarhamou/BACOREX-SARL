from django.urls import path

from . import views

urlpatterns = [
    path('', views.listeMateriel, name = 'listeMateriel'),
    path('newentrepot', views.newEntrepot, name='newentrepot'),
    path('listentrepot', views.listEntrepot, name='listentrepot'),
    path('newcategorie',views.newCategorie, name='newcategorie'),
    path('listeCategorie',views.listeCategorie, name='listeCategorie'),
]