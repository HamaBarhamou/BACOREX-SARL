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

    path('projects/<int:project_id>/phases/', views.list_phases_for_project, name='list_phases_for_project'),
    path('projects/<int:project_id>/phases/new/', views.new_phase_for_project, name='new_phase_for_project'),
    path('phases/<int:phase_id>/<int:projet_id>/', views.phase_detail, name='phase_detail'),
    path('phases/<int:phase_id>/<int:projet_id>/edit/', views.edit_phase, name='edit_phase'),
    path('phases/<int:phase_id>/<int:projet_id>/delete/', views.delete_phase, name='delete_phase'),
    
    #path('revue-portefeuille/', views.revue_portefeuille, name='revue_portefeuille'),
    path('display/', views.display_projet_data, name='display_data'),
    path('download/', views.download_projet_data, name='download_data'),
]
