from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import (
    DAOForm,
    ExperienceSimilaireForm,
    ReponseDAOForm,
    RapportDepouillementForm,
    LigneRapportForm,
    OffreLotForm,
    LotFormSet,
    LigneRapportFormSet,
    OffreLotFormSet,
)
from django.template import loader
from .models import (
    DAO,
    ExperienceSimilaire,
    Lot,
    ReponseDAO,
    RapportDepouillement,
    LigneRapport,
    OffreLot,
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


def dao_list(request):
    daos = DAO.objects.all()
    return render(request, "dao/dao_list.html", {"daos": daos})


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


def reponse_dao_list(request):
    reponses = ReponseDAO.objects.all()  # Récupère toutes les réponses DAO
    return render(request, "dao/reponse_dao_list.html", {"reponses": reponses})


def rapport_depouillement_list(request):
    rapports = RapportDepouillement.objects.all()  # Récupère tous les rapports
    return render(
        request, "dao/rapport_depouillement_list.html", {"rapports": rapports}
    )


def lot_list(request):
    lots = Lot.objects.all()
    return render(request, "dao/lot_list.html", {"lots": lots})


def lot_delete(request, pk):
    lot = get_object_or_404(Lot, pk=pk)
    if request.method == "POST":
        lot.delete()
        return redirect("lot_list")
    return render(request, "dao/lot_confirm_delete.html", {"lot": lot})


def reponse_dao_list(request):
    reponses = ReponseDAO.objects.all()
    return render(request, "dao/reponse_dao_list.html", {"reponses": reponses})


def reponse_dao_create(request):
    if request.method == "POST":
        form = ReponseDAOForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("reponse_dao_list")
    else:
        form = ReponseDAOForm()
    return render(request, "dao/reponse_dao_form.html", {"form": form})


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


def reponse_dao_delete(request, pk):
    reponse = get_object_or_404(ReponseDAO, pk=pk)
    if request.method == "POST":
        reponse.delete()
        return redirect("reponse_dao_list")
    return render(request, "dao/reponse_dao_confirm_delete.html", {"reponse": reponse})


def rapport_depouillement_manage(request, dao_pk):
    dao = get_object_or_404(DAO, pk=dao_pk)
    rapport = RapportDepouillement.objects.filter(dao=dao).first()

    if rapport:
        return redirect("dao:rapport_depouillement_update", pk=rapport.pk)
    else:
        return redirect("dao:rapport_depouillement_create", dao_pk=dao_pk)


def rapport_depouillement_create(request, dao_pk):
    dao = get_object_or_404(DAO, pk=dao_pk)
    lots = dao.lots.all()

    # Préparer les données des offres
    offres_data = {}

    if request.method == "POST":
        form = RapportDepouillementForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    rapport = form.save()
                    formset = LigneRapportFormSet(request.POST, instance=rapport)
                    if formset.is_valid():
                        lignes = formset.save()
                        # Gérer les offres pour chaque ligne
                        for ligne in lignes:
                            offre_formset = OffreLotFormSet(
                                request.POST,
                                instance=ligne,
                                prefix=f"offres_{ligne.id}",
                            )
                            if offre_formset.is_valid():
                                offre_formset.save()
                            else:
                                raise ValueError("Erreur dans les offres")

                        messages.success(
                            request, "Rapport de dépouillement créé avec succès."
                        )
                        return redirect("dao:dao_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de la création: {str(e)}")
    else:
        form = RapportDepouillementForm(initial={"dao": dao})
        formset = LigneRapportFormSet()

    # Pour chaque lot et chaque ligne, préparer les données d'offre
    for ligne_form in formset:
        for lot in lots:
            key = f"offres_{ligne_form.instance.pk}_{lot.pk}"
            offres_data[key] = {"lot": lot, "offre_financiere": None}

    context = {
        "form": form,
        "formset": formset,
        "dao": dao,
        "lots": lots,
        "offres_data": offres_data,
    }
    return render(request, "dao/rapport_depouillement_form.html", context)


def rapport_depouillement_update(request, pk):
    rapport = get_object_or_404(RapportDepouillement, pk=pk)
    lots = rapport.dao.lots.all()

    # Préparer les données des offres existantes
    offres_data = {}

    if request.method == "POST":
        form = RapportDepouillementForm(request.POST, instance=rapport)
        if form.is_valid():
            try:
                with transaction.atomic():
                    rapport = form.save()
                    formset = LigneRapportFormSet(request.POST, instance=rapport)
                    if formset.is_valid():
                        lignes = formset.save()
                        for ligne in lignes:
                            offre_formset = OffreLotFormSet(
                                request.POST,
                                instance=ligne,
                                prefix=f"offres_{ligne.id}",
                            )
                            if offre_formset.is_valid():
                                offre_formset.save()
                            else:
                                raise ValueError("Erreur dans les offres")

                        messages.success(
                            request, "Rapport de dépouillement mis à jour avec succès."
                        )
                        return redirect("dao:dao_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de la mise à jour: {str(e)}")
    else:
        form = RapportDepouillementForm(instance=rapport)
        formset = LigneRapportFormSet(instance=rapport)

        # Récupérer les offres existantes
        for ligne_form in formset:
            for lot in lots:
                offre = lot.offres.filter(ligne_rapport=ligne_form.instance).first()
                key = f"offres_{ligne_form.instance.pk}_{lot.pk}"
                offres_data[key] = {
                    "lot": lot,
                    "offre_financiere": offre.offre_financiere if offre else None,
                }

    context = {
        "form": form,
        "formset": formset,
        "rapport": rapport,
        "dao": rapport.dao,
        "lots": lots,
        "offres_data": offres_data,
    }
    return render(request, "dao/rapport_depouillement_form.html", context)


def rapport_depouillement_list(request):
    rapports = RapportDepouillement.objects.all()
    return render(
        request, "dao/rapport_depouillement_list.html", {"rapports": rapports}
    )


def rapport_depouillement_delete(request, pk):
    rapport = get_object_or_404(RapportDepouillement, pk=pk)
    if request.method == "POST":
        rapport.delete()
        return redirect("rapport_depouillement_list")
    return render(
        request, "dao/rapport_depouillement_confirm_delete.html", {"rapport": rapport}
    )


def ligne_rapport_list(request):
    lignes = LigneRapport.objects.all()
    return render(request, "dao/ligne_rapport_list.html", {"lignes": lignes})


def ligne_rapport_create(request):
    if request.method == "POST":
        form = LigneRapportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ligne_rapport_list")
    else:
        form = LigneRapportForm()
    return render(request, "dao/ligne_rapport_form.html", {"form": form})


def ligne_rapport_update(request, pk):
    ligne = get_object_or_404(LigneRapport, pk=pk)
    if request.method == "POST":
        form = LigneRapportForm(request.POST, instance=ligne)
        if form.is_valid():
            form.save()
            return redirect("ligne_rapport_list")
    else:
        form = LigneRapportForm(instance=ligne)
    return render(request, "dao/ligne_rapport_form.html", {"form": form})


def ligne_rapport_delete(request, pk):
    ligne = get_object_or_404(LigneRapport, pk=pk)
    if request.method == "POST":
        ligne.delete()
        return redirect("ligne_rapport_list")
    return render(request, "dao/ligne_rapport_confirm_delete.html", {"ligne": ligne})


def offre_lot_list(request):
    offres = OffreLot.objects.all()
    return render(request, "dao/offre_lot_list.html", {"offres": offres})


def offre_lot_create(request):
    if request.method == "POST":
        form = OffreLotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("offre_lot_list")
    else:
        form = OffreLotForm()
    return render(request, "dao/offre_lot_form.html", {"form": form})


def offre_lot_update(request, pk):
    offre = get_object_or_404(OffreLot, pk=pk)
    if request.method == "POST":
        form = OffreLotForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect("offre_lot_list")
    else:
        form = OffreLotForm(instance=offre)
    return render(request, "dao/offre_lot_form.html", {"form": form})


def offre_lot_delete(request, pk):
    offre = get_object_or_404(OffreLot, pk=pk)
    if request.method == "POST":
        offre.delete()
        return redirect("offre_lot_list")
    return render(request, "dao/offre_lot_confirm_delete.html", {"offre": offre})
