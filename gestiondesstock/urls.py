from django.urls import path
from . import views


app_name = 'stockmanagement'

urlpatterns = [
    path('', views.listeMateriel, name = 'materialinventory'),
    path('newentrepot', views.newEntrepot, name='newwarehouse'),
    path('listentrepot', views.listEntrepot, name='warehouselist'),
    path('newcategorie',views.newCategorie, name='newcategory'),
    path('listeCategorie',views.listeCategorie, name='categorylist'),
    path('newmateriel', views.newMateriel, name='newmaterial'),
    path('newmateriel/<int:pk>/edit/', views.editMateriel, name='materiel_edit'),
    path('newmateriel/<int:pk>/delette/', views.deletteMateriel, name='deletteMateriel'),
]