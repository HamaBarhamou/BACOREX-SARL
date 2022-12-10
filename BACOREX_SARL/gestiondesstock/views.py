from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
def newMateriel(request):
    if request.method == 'POST':
        form = MaterielsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            qte = form.cleaned_data["qte"]
            categorie = form.cleaned_data["categorie"]
            entrepot = form.cleaned_data["entrepot"]
            image = form.cleaned_data["image"]
            
            materiel = Materiels(
                                 name = name, 
                                 description = description,
                                 qte = qte,
                                 categorie = categorie,
                                 entrepot = entrepot,
                                 image = image
                                 )
            
            materiel.save()
            print("MA:",materiel)
            form = MaterielsForm()
        else:
            print("Données formulaire Non valid") 
    else:
        form = MaterielsForm() 

    context = {'form':form}
    template = loader.get_template('newMateriel.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def editMateriel(request, pk):
    materiel = Materiels.objects.get(pk=pk)
    if request.method == "POST":
        form = MaterielsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            qte = form.cleaned_data["qte"]
            categorie = form.cleaned_data["categorie"]
            entrepot = form.cleaned_data["entrepot"]
            image = form.cleaned_data["image"]

            materiel.name = name,
            materiel.description = description,
            materiel.qte = qte,
            materiel.categorie = categorie,
            materiel.entrepot = entrepot,
            materiel.image = image

            #materiel.save()
            print("mat::",materiel.name)
            return redirect('listeMateriel')
    else:
        form = MaterielsForm(instance=materiel)
        context = {'form':form}
        template = loader.get_template('newMateriel.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def listeMateriel(request):
    context = {'materiel': Materiels.objects.all()}
    template = loader.get_template('listeMateriels.html')
    return HttpResponse(template.render(context, request))