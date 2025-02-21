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
    path("dao/", views.dao_list, name="dao_list"),  # URL pour la liste des DAO
    path("dao_create/", views.dao_create, name="dao_create"),
    path("dao_update/<int:pk>", views.dao_update, name="dao_update"),
    path(
        "dao/<int:pk>/delete/", views.dao_delete, name="dao_delete"
    ),  # format plus cohérent
    path("reponse-dao/", views.reponse_dao_list, name="reponse_dao_list"),
    path(
        "rapport-depouillement/",
        views.rapport_depouillement_list,
        name="rapport_depouillement_list",
    ),
    path("lot/", views.lot_list, name="lot_list"),
    path("lot/create/", views.lot_create, name="lot_create"),
    path("lot/update/<int:pk>/", views.lot_update, name="lot_update"),
    path("lot/delete/<int:pk>/", views.lot_delete, name="lot_delete"),
    path("reponse-dao/", views.reponse_dao_list, name="reponse_dao_list"),
    path("reponse-dao/create/", views.reponse_dao_create, name="reponse_dao_create"),
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
        "rapport-depouillement/",
        views.rapport_depouillement_list,
        name="rapport_depouillement_list",
    ),
    path(
        "rapport-depouillement/create/",
        views.rapport_depouillement_create,
        name="rapport_depouillement_create",
    ),
    path(
        "rapport-depouillement/update/<int:pk>/",
        views.rapport_depouillement_update,
        name="rapport_depouillement_update",
    ),
    path(
        "rapport-depouillement/delete/<int:pk>/",
        views.rapport_depouillement_delete,
        name="rapport_depouillement_delete",
    ),
    path("ligne-rapport/", views.ligne_rapport_list, name="ligne_rapport_list"),
    path(
        "ligne-rapport/create/", views.ligne_rapport_create, name="ligne_rapport_create"
    ),
    path(
        "ligne-rapport/update/<int:pk>/",
        views.ligne_rapport_update,
        name="ligne_rapport_update",
    ),
    path(
        "ligne-rapport/delete/<int:pk>/",
        views.ligne_rapport_delete,
        name="ligne_rapport_delete",
    ),
    path("offre-lot/", views.offre_lot_list, name="offre_lot_list"),
    path("offre-lot/create/", views.offre_lot_create, name="offre_lot_create"),
    path("offre-lot/update/<int:pk>/", views.offre_lot_update, name="offre_lot_update"),
    path("offre-lot/delete/<int:pk>/", views.offre_lot_delete, name="offre_lot_delete"),
]
