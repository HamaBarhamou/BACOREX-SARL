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
    path("dao/", views.dao_list, name="dao_list"),
    path("dao_create/", views.dao_create, name="dao_create"),
    path("dao_update/<int:pk>", views.dao_update, name="dao_update"),
    path(
        "dao/<int:pk>/delete/", views.dao_delete, name="dao_delete"
    ),  # format plus cohérent
    path(
        "reponse-dao/update/<int:pk>/",
        views.reponse_dao_update,
        name="reponse_dao_update",
    ),
    path(
        "dao/<int:dao_id>/reponse/", views.reponse_dao_manage, name="reponse_dao_manage"
    ),
    path(
        "reponse-dao/delete/<int:pk>/",
        views.reponse_dao_delete,
        name="reponse_dao_delete",
    ),
    path(
        "rapport-depouillement/manage/<int:dao_pk>/",
        views.rapport_depouillement_manage,
        name="rapport_depouillement_manage",
    ),
    path(
        "rapport-depouillement/create/<int:dao_pk>/",
        views.rapport_depouillement_create,
        name="rapport_depouillement_create",
    ),
    path(
        "rapport-depouillement/update/<int:pk>/",
        views.rapport_depouillement_update,
        name="rapport_depouillement_update",
    ),
    path(
        "rapport/<int:pk>/view/",
        views.rapport_depouillement_view,
        name="rapport_depouillement_view",
    ),
    path(
        "dao/<int:dao_id>/attributions/",
        views.gestion_attributions,
        name="gestion_attributions",
    ),
    path(
        "lot/<int:lot_id>/attribution/ajouter/",
        views.ajouter_attribution,
        name="ajouter_attribution",
    ),
    path(
        "attribution/<int:attribution_id>/modifier/",
        views.modifier_attribution,
        name="modifier_attribution",
    ),
    path(
        "attribution/<int:attribution_id>/supprimer/",
        views.supprimer_attribution,
        name="supprimer_attribution",
    ),
]
