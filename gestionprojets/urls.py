from django.urls import path

from . import views

urlpatterns = [
    path('', views.listeProject, name='listeproject'),
    path('listeclient', views.listeClient, name='listeclient'),
    path('newclient', views.newClient, name='newclient'),
    path('newprojet', views.newProjet, name='newprojet'),
    path('<int:pk>', views.detailProject, name='detailprojet'),
    path(
        '<int:pk>/intervenants',
        views.List_Intervenant_Project,
        name='List_Intervenant_Project'
        ),
]
