from django.urls import path

from . import views

app_name = 'projectmanagement'

urlpatterns = [
    path('', views.listeProject, name='projectlist'),
    path('listeclient', views.listeClient, name='clientlist'),
    path('newclient', views.newClient, name='newclient'),
    path('newprojet', views.newProjet, name='newproject'),
    path('newprojet/<int:pk>/edit/', views.editProjet, name='editProjet'),
    path('newprojet/<int:pk>/delete/', views.deletteProjet, name='deleteProjet'),
    path('<int:pk>', views.detailProject, name='detailprojet'),
    path(
        '<int:pk>/intervenants',
        views.List_Intervenant_Project,
        name='List_Intervenant_Project'
        ),
    path('<int:pk>/newTask', views.newTask, name='newTask'),
    path('editTask/<int:pk>/', views.editTask, name='editTask'),
    path('deleteTask/<int:pk>/', views.deleteTask, name='deleteTask'),

]
