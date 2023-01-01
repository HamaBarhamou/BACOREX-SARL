from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from .forms import ClientForm, ProjetForm, TaskForm
from .models import Client, Projet
from plannig.models import Event

fonction = [
                '',
                'Assistant DAO',
                'Chef Service Etude',
                'Chef Departement Etude',
                'Directeur Generale',
                'admin',
                'Coordinateur des Operations',
                'Conducteurs des Travaux',
                'Chef de Projet',
                'DEGP',
                'Magasinier',
                'Intervenant',
               ]


# Create your views here.
@login_required(login_url='/user/')
def newClient(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            materiel = form.save()
            return redirect('listeclient')
    else:
        form = ClientForm()
        context = {'form': form}
        template = loader.get_template('newclient.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def listeClient(request):
    context = {'clients': Client.objects.all()}
    template = loader.get_template('listeclient.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def newProjet(request):
    if request.method == "POST":
        form = ProjetForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProjetForm()
        else:
            form = ProjetForm(request.POST)
    else:
        form = ProjetForm()
    context = {'form': form}
    template = loader.get_template('newprojet.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def editProjet(request, pk):
    projet = Projet.objects.get(pk=pk)
    if request.method == "POST":
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            projet = form.save()
            return redirect('listeproject')
    else:
        form = ProjetForm(instance=projet)
        context = {'form': form, 'pk': projet.pk}
        template = loader.get_template('editProjet.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def deletteProjet(request, pk):
    Projet.objects.get(pk=pk).delete()
    return redirect('listeproject')


@login_required(login_url='/user/')
def listeProject(request):
    Directeur_Generale = 4
    Admin = 5
    Coordinateur_des_Operations = 6
    Conducteurs_des_Travaux = 7
    Chef_de_Projet = 8
    Intervenant = 11

    leader = [Directeur_Generale, Admin, Coordinateur_des_Operations]
    if request.user.fonction in leader:
        projets = Projet.objects.all().values()
    elif request.user.fonction == Chef_de_Projet:
        projets = Projet.objects.filter(chef_project=request.user).values()
    elif request.user.fonction == Conducteurs_des_Travaux:
        projets = Projet.objects.filter(conducteur_travaux=request.user).values()

    context = {'projets': projets}
    template = loader.get_template('listeproject.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def detailProject(request, pk):
    status = ['', 'NON DÉBUTÉ', 'EN COURS' ,'TERMINER', 'ARCHIVER']
    projet = Projet.objects.get(pk=pk)
    context = {'projet': projet, 'status': status[projet.status], 'pk': pk}
    template = loader.get_template('detailProjet.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def List_Intervenant_Project(request, pk):
    status = ['', 'NON DÉBUTÉ', 'EN COURS' ,'TERMINER', 'ARCHIVER']
    projet = Projet.objects.get(pk=pk)
    intervenant = [
                    projet.coordinateur,
                    projet.chef_project,
                    projet.conducteur_travaux,
                  ]

    for loop in Projet.objects.get(pk=pk).list_intervenant.all():
        intervenant.append(loop)
    
    context = {
                'projet': projet,
                'status': status[projet.status],
                'pk': pk,
                'intervenant': intervenant,
                'fonction': fonction
              }
    template = loader.get_template('intervenantProjet.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def newTask(request, pk):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form = TaskForm()
        else:
            form = TaskForm(request.POST)
    else:
        form = TaskForm()
    context = {'form': form, 'pk': pk}
    template = loader.get_template('newTask.html')
    return HttpResponse(template.render(context, request))