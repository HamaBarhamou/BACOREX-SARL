from django.urls import path
from . import views


app_name = 'gestiondesstock'

urlpatterns = [
    path('', views.listeMateriel, name = 'listeMateriel'),
    path('newentrepot', views.newEntrepot, name='newentrepot'),
    path('listentrepot', views.listEntrepot, name='listentrepot'),
    path('newcategorie',views.newCategorie, name='newcategorie'),
    path('listeCategorie',views.listeCategorie, name='listeCategorie'),
    path('newmateriel', views.newMateriel, name='newmateriel'),
    path('newmateriel/<int:pk>/edit/', views.editMateriel, name='materiel_edit'),
    path('newmateriel/<int:pk>/delette/', views.deletteMateriel, name='deletteMateriel'),
]