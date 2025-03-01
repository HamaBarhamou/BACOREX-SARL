from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime
from .forms import (
    DAOForm,
    ExperienceSimilaireForm,
    ReponseDAOForm,
    RapportDepouillementForm,
    LotFormSet,
    LigneRapportFormSet,
)
from django.template import loader
from .models import (
    DAO,
    ExperienceSimilaire,
    ReponseDAO,
    RapportDepouillement,
    OffreLot,
    Soumissionnaire,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction


@login_required(login_url="/user/")
def home_dao(request):
    dao = DAO.objects.all().values()
    context = {"dao": dao}
    template = loader.get_template("home_dao.html")
    return HttpResponse(template.render(context, request))


@login_required(login_url="/user/")
def add_dao(request):
    if request.method == "POST":
        form = DAOForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DAOForm()

    context = {"form": form}
    template = loader.get_template("add_dao.html")
    return HttpResponse(template.render(context, request))


@login_required(login_url="/user/")
def create_experience_similaire(request):
    if request.method == "POST":
        form = ExperienceSimilaireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dao:experience_similaire_list")
    else:
        form = ExperienceSimilaireForm()
    return render(request, "dao/experience_similaire_form.html", {"form": form})


@login_required(login_url="/user/")
def experience_similaire_list(request):
    experiences = ExperienceSimilaire.objects.all()
    return render(
        request, "dao/experience_similaire_list.html", {"experiences": experiences}
    )


@login_required(login_url="/user/")
def experience_similaire_detail(request, pk):
    experience = get_object_or_404(ExperienceSimilaire, pk=pk)
    return render(
        request, "dao/experience_similaire_detail.html", {"experience": experience}
    )


@login_required(login_url="/user/")
def update_experience_similaire(request, pk):
    experience = get_object_or_404(ExperienceSimilaire, pk=pk)
    if request.method == "POST":
        form = ExperienceSimilaireForm(request.POST, request.FILES, instance=experience)
        if form.is_valid():
            form.save()
            return redirect("dao:experience_similaire_detail", pk=experience.pk)
    else:
        form = ExperienceSimilaireForm(instance=experience)
    return render(request, "dao/experience_similaire_form.html", {"form": form})


@login_required(login_url="/user/")
def delete_experience_similaire(request, pk):
    experience = get_object_or_404(ExperienceSimilaire, pk=pk)
    if request.method == "POST":
        experience.delete()
        return redirect("dao:experience_similaire_list")
    return render(
        request,
        "dao/experience_similaire_confirm_delete.html",
        {"experience": experience},
    )


@login_required(login_url="/user/")
def dao_list(request):
    # Récupération des paramètres de filtrage
    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")
    date_debut = request.GET.get("date_debut", "")
    date_fin = request.GET.get("date_fin", "")

    # Base de la requête
    daos = DAO.objects.all().order_by("-date_publication")

    # Appliquer les filtres
    if search_query:
        daos = daos.filter(
            Q(dao_number__icontains=search_query) | Q(dao_title__icontains=search_query)
        )

    if status_filter:
        if status_filter == "open":
            daos = daos.filter(is_closed=False)
        elif status_filter == "closed":
            daos = daos.filter(is_closed=True)

    # Filtrage par plage de dates
    if date_debut:
        date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d").date()
        daos = daos.filter(
            Q(date_publication__date__gte=date_debut_obj)
            | Q(date_soumission__date__gte=date_debut_obj)
        )

    if date_fin:
        date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d").date()
        daos = daos.filter(
            Q(date_publication__date__lte=date_fin_obj)
            | Q(date_soumission__date__lte=date_fin_obj)
        )

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(daos, 10)  # 10 éléments par page

    try:
        daos = paginator.page(page)
    except PageNotAnInteger:
        daos = paginator.page(1)
    except EmptyPage:
        daos = paginator.page(paginator.num_pages)

    # Contexte avec la date actuelle
    context = {"daos": daos, "now": datetime.now()}

    return render(request, "dao/dao_list.html", context)


@login_required(login_url="/user/")
def dao_create(request):
    if request.method == "POST":
        form = DAOForm(request.POST, request.FILES)
        formset = LotFormSet(request.POST, instance=DAO())

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    dao = form.save()
                    formset.instance = dao
                    formset.save()
                messages.success(request, "DAO et lots créés avec succès.")
                return redirect("dao:dao_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de la création: {str(e)}")
    else:
        form = DAOForm()
        formset = LotFormSet(instance=DAO())

    return render(
        request, "dao/dao_create_form.html", {"form": form, "formset": formset}
    )


@login_required(login_url="/user/")
def dao_update(request, pk):
    dao = get_object_or_404(DAO, pk=pk)
    if request.method == "POST":
        form = DAOForm(request.POST, request.FILES, instance=dao)
        formset = LotFormSet(request.POST, instance=dao)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    dao = form.save()
                    formset.save()
                messages.success(request, "DAO et lots mis à jour avec succès.")
                return redirect("dao:dao_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de la mise à jour: {str(e)}")
    else:
        form = DAOForm(instance=dao)
        formset = LotFormSet(instance=dao)

    return render(
        request,
        "dao/dao_create_form.html",
        {"form": form, "formset": formset, "is_update": True},
    )


@login_required(login_url="/user/")
def dao_delete(request, pk):
    dao = get_object_or_404(DAO, pk=pk)
    if request.method == "POST":
        try:
            dao.delete()
            messages.success(
                request, f"Le DAO {dao.dao_number} a été supprimé avec succès."
            )
        except Exception as e:
            messages.error(request, "Une erreur s'est produite lors de la suppression.")
    return redirect("dao:dao_list")


@login_required(login_url="/user/")
def reponse_dao_manage(request, dao_id):
    dao = get_object_or_404(DAO, pk=dao_id)
    reponse = ReponseDAO.objects.filter(dao=dao).first()

    if request.method == "POST":
        if reponse:
            form = ReponseDAOForm(request.POST, request.FILES, instance=reponse)
        else:
            form = ReponseDAOForm(request.POST, request.FILES)

        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.dao = dao
            reponse.save()
            messages.success(request, "Offre enregistrée avec succès.")
            return redirect("dao:dao_list")
    else:
        form = ReponseDAOForm(instance=reponse if reponse else None)

    return render(
        request,
        "dao/reponse_dao_form.html",
        {"form": form, "dao": dao, "reponse": reponse},
    )


@login_required(login_url="/user/")
def reponse_dao_update(request, pk):
    reponse = get_object_or_404(ReponseDAO, pk=pk)
    if request.method == "POST":
        form = ReponseDAOForm(request.POST, request.FILES, instance=reponse)
        if form.is_valid():
            form.save()
            return redirect("reponse_dao_list")
    else:
        form = ReponseDAOForm(instance=reponse)
    return render(request, "dao/reponse_dao_form.html", {"form": form})


@login_required(login_url="/user/")
def reponse_dao_delete(request, pk):
    reponse = get_object_or_404(ReponseDAO, pk=pk)
    if request.method == "POST":
        reponse.delete()
        return redirect("reponse_dao_list")
    return render(request, "dao/reponse_dao_confirm_delete.html", {"reponse": reponse})


@login_required(login_url="/user/")
def rapport_depouillement_manage(request, dao_pk):
    dao = get_object_or_404(DAO, pk=dao_pk)
    rapport = RapportDepouillement.objects.filter(dao=dao).first()

    if rapport:
        return redirect("dao:rapport_depouillement_view", pk=rapport.pk)
    else:
        return redirect("dao:rapport_depouillement_create", dao_pk=dao_pk)


@login_required(login_url="/user/")
def rapport_depouillement_create(request, dao_pk):
    dao = get_object_or_404(DAO, pk=dao_pk)
    lots = dao.lots.all()

    if request.method == "POST":
        form = RapportDepouillementForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    rapport = form.save(commit=False)
                    rapport.dao = dao
                    rapport.save()

                    formset = LigneRapportFormSet(request.POST, instance=rapport)
                    if formset.is_valid():
                        # Supprimer les lignes marquées pour suppression
                        formset.save(commit=False)
                        for obj in formset.deleted_objects:
                            obj.delete()

                        for i, ligne_form in enumerate(formset.forms):
                            if ligne_form.cleaned_data.get("DELETE"):
                                continue

                            ligne = ligne_form.save(commit=False)

                            # Gérer le soumissionnaire
                            nouveau_soumissionnaire = request.POST.get(
                                f"lignes-{i}-nouveau_soumissionnaire"
                            )
                            if nouveau_soumissionnaire:
                                (
                                    soumissionnaire,
                                    created,
                                ) = Soumissionnaire.objects.get_or_create(
                                    nom=nouveau_soumissionnaire
                                )
                                ligne.soumissionnaire = soumissionnaire
                            ligne.save()

                            # Maintenant nous allons collecter manuellement les données des offres
                            for j, lot in enumerate(lots):
                                offre_financiere = request.POST.get(
                                    f"offres_{i}-{j}-offre_financiere"
                                )
                                if offre_financiere and offre_financiere.strip():
                                    try:
                                        offre_financiere = Decimal(
                                            offre_financiere.replace(",", ".")
                                        )
                                        OffreLot.objects.update_or_create(
                                            ligne_rapport=ligne,
                                            lot=lot,
                                            defaults={
                                                "offre_financiere": offre_financiere
                                            },
                                        )
                                    except (ValueError, InvalidOperation):
                                        # Si la conversion en Decimal échoue, ignorez cette entrée
                                        pass

                        messages.success(
                            request, "Rapport de dépouillement créé avec succès."
                        )
                        return redirect("dao:dao_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de la création: {str(e)}")
    else:
        form = RapportDepouillementForm(initial={"dao": dao})
        formset = LigneRapportFormSet()

    # Préparer les données pour le template
    lignes_existantes = []
    if hasattr(formset, "instance") and formset.instance.pk:
        lignes_existantes = formset.instance.lignes.all()

    context = {
        "form": form,
        "formset": formset,
        "dao": dao,
        "lots": lots,
        "lignes_existantes": lignes_existantes,
        "rapport": None,
        "ligne_offres": None,
    }
    return render(request, "dao/rapport_depouillement_form.html", context)


@login_required(login_url="/user/")
def rapport_depouillement_update(request, pk):
    rapport = get_object_or_404(RapportDepouillement, pk=pk)
    dao = rapport.dao
    lots = dao.lots.all()

    # Préparer les offres existantes sous forme de dictionnaire pour un accès facile
    ligne_offres = {}
    for ligne in rapport.lignes.all():
        ligne_offres[ligne.id] = {}
        for offre in ligne.offres_lots.all():
            ligne_offres[ligne.id][offre.lot.id] = offre.offre_financiere

    if request.method == "POST":
        form = RapportDepouillementForm(request.POST, instance=rapport)
        if form.is_valid():
            try:
                with transaction.atomic():
                    rapport = form.save()
                    formset = LigneRapportFormSet(request.POST, instance=rapport)
                    if formset.is_valid():
                        # Supprimer les lignes marquées pour suppression
                        formset.save(commit=False)
                        for obj in formset.deleted_objects:
                            obj.delete()

                        for i, ligne_form in enumerate(formset.forms):
                            if ligne_form.cleaned_data.get("DELETE"):
                                continue

                            ligne = ligne_form.save(commit=False)

                            # Gérer le soumissionnaire
                            nouveau_soumissionnaire = request.POST.get(
                                f"lignes-{i}-nouveau_soumissionnaire", ""
                            ).strip()
                            soumissionnaire_id = ligne_form.cleaned_data.get(
                                "soumissionnaire"
                            )

                            if nouveau_soumissionnaire:
                                # Utiliser un nouveau soumissionnaire
                                (
                                    soumissionnaire,
                                    created,
                                ) = Soumissionnaire.objects.get_or_create(
                                    nom=nouveau_soumissionnaire
                                )
                                ligne.soumissionnaire = soumissionnaire
                            elif soumissionnaire_id:
                                # Le soumissionnaire existant est déjà défini par le formulaire
                                pass
                            else:
                                # Aucun soumissionnaire n'est spécifié
                                messages.warning(
                                    request,
                                    f"Une ligne sans soumissionnaire a été ignorée.",
                                )
                                continue

                            ligne.save()

                            # Maintenant nous allons collecter manuellement les données des offres
                            for j, lot in enumerate(lots):
                                offre_financiere = request.POST.get(
                                    f"offres_{i}-{j}-offre_financiere"
                                )
                                if offre_financiere and offre_financiere.strip():
                                    try:
                                        offre_financiere = Decimal(
                                            offre_financiere.replace(",", ".")
                                        )
                                        OffreLot.objects.update_or_create(
                                            ligne_rapport=ligne,
                                            lot=lot,
                                            defaults={
                                                "offre_financiere": offre_financiere
                                            },
                                        )
                                    except (ValueError, InvalidOperation):
                                        # Si la conversion en Decimal échoue, ignorez cette entrée
                                        pass

                        messages.success(
                            request, "Rapport de dépouillement mis à jour avec succès."
                        )
                        return redirect("dao:rapport_depouillement_view", pk=rapport.pk)
                        # return redirect("dao:dao_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de la mise à jour: {str(e)}")
    else:
        form = RapportDepouillementForm(instance=rapport)
        formset = LigneRapportFormSet(instance=rapport)

    # Préparer les données pour le template
    lignes_existantes = rapport.lignes.all()

    context = {
        "form": form,
        "formset": formset,
        "rapport": rapport,
        "dao": dao,
        "lots": lots,
        "lignes_existantes": lignes_existantes,
        "ligne_offres": ligne_offres,
    }
    return render(request, "dao/rapport_depouillement_form.html", context)


@login_required(login_url="/user/")
def rapport_depouillement_view(request, pk):
    rapport = get_object_or_404(RapportDepouillement, pk=pk)
    dao = rapport.dao
    lots = dao.lots.all()
    lignes = rapport.lignes.all()

    # Restructurer les données pour faciliter l'accès dans le template
    ligne_offres = {}
    for ligne in lignes:
        ligne_offres[ligne.id] = {
            "ligne_id": ligne.id
        }  # Inclure l'ID de ligne directement
        for offre in ligne.offres_lots.all():
            ligne_offres[ligne.id][offre.lot.id] = offre.offre_financiere

    context = {
        "rapport": rapport,
        "dao": dao,
        "lots": lots,
        "lignes": lignes,
        "ligne_offres": ligne_offres,
    }
    return render(request, "dao/rapport_depouillement_view.html", context)
