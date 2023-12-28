"""BACOREX_SARL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "dao/", include("dao.urls", namespace="dao")
    ),  # Ajoutez l'espace de noms "dao" pour l'application "dao"
    path(
        "user/", include("userprofile.urls", namespace="userprofile")
    ),  # Ajoutez l'espace de noms "userprofile" pour l'application "userprofile"
    path(
        "boitereception/", include("gestioncouriers.urls", namespace="gestioncouriers")
    ),  # Ajoutez l'espace de noms "gestioncouriers" pour l'application "gestioncouriers"
    path(
        "magasin/", include("gestiondesstock.urls", namespace="gestiondesstock")
    ),  # Ajoutez l'espace de noms "gestiondesstock" pour l'application "gestiondesstock"
    path(
        "projet/", include("gestionprojets.urls", namespace="gestionprojets")
    ),  # Ajoutez l'espace de noms "gestionprojets" pour l'application "gestionprojets"
    path(
        "plannig/", include("plannig.urls", namespace="plannig")
    ),  # Ajoutez l'espace de noms "plannig" pour l'application "plannig"
    path("history/", include("history.urls", namespace="history")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
