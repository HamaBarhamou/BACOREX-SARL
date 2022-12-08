from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .forms import CategoriMaterielForm, MaterielsForm, EntrepotForm
from .models import CategoriMateriel, Materiels, Entrepot

# Create your views here.
@login_required(login_url='/user/')
def newEntrepot(request):
    if request.method == 'POST':
        form = EntrepotForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            adresse = form.cleaned_data["adresse"]
            entrepot = Entrepot(name = name, adresse = adresse)
            
            entrepot.save()
            print(entrepot.name)
            form = EntrepotForm()
    else:
        form = EntrepotForm()

    context = {'form':form}
    template = loader.get_template('newEntrepot.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def listEntrepot(request):
    e = Entrepot.objects.all()
    context = {'entrepot': e}
    template = loader.get_template('listeEntrepot.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def listeCategorie(request):
    context = {'categorie': CategoriMateriel.objects.all()}
    template = loader.get_template('listeCategorie.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def newCategorie(request):
    if request.method == 'POST':
        form = CategoriMaterielForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            categorie = CategoriMateriel(name = name, description = description)
            
            categorie.save()
            form = CategoriMaterielForm()
    else:
        form = CategoriMaterielForm()

    context = {'form':form}
    template = loader.get_template('newCategorie.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def listeMateriel(request):
    context = {}
    template = loader.get_template('listeMateriels.html')
    return HttpResponse(template.render(context, request))