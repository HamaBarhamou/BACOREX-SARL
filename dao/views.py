from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import DaoForm, ExperienceSimilaireForm
from django.template import loader
from .models import DAO, ExperienceSimilaire
from django.contrib.auth.decorators import login_required


@login_required(login_url="/user/")
def home_dao(request):
    dao = DAO.objects.all().values()
    context = {"dao": dao}
    template = loader.get_template("home_dao.html")
    return HttpResponse(template.render(context, request))


@login_required(login_url="/user/")
def add_dao(request):
    if request.method == "POST":
        form = DaoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DaoForm()

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
