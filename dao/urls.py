from django.urls import path
from . import views

app_name = "dao"

urlpatterns = [
    path("", views.home_dao, name="home_dao"),
    path("add/", views.add_dao, name="add_dao"),
    path(
        "experience_similaires/",
        views.experience_similaire_list,
        name="experience_similaire_list",
    ),
    path(
        "experience_similaires/new/",
        views.create_experience_similaire,
        name="create_experience_similaire",
    ),
    path(
        "experience_similaires/<int:pk>/",
        views.experience_similaire_detail,
        name="experience_similaire_detail",
    ),
    path(
        "experience_similaires/<int:pk>/edit/",
        views.update_experience_similaire,
        name="update_experience_similaire",
    ),
    path(
        "experience_similaires/<int:pk>/delete/",
        views.delete_experience_similaire,
        name="delete_experience_similaire",
    ),
]
