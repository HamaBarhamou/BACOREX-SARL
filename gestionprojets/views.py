from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from .forms import ClientForm, ProjetForm
from .models import Client, Projet
from plannig.models import Event


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
            """ return redirect('listeproject') """
            form = ProjetForm()
        else:
            form = ProjetForm(request.POST)
    else:
        form = ProjetForm()
    context = {'form': form}
    template = loader.get_template('newprojet.html')
    return HttpResponse(template.render(context, request))


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
    status = ['NON DÉBUTÉ', 'EN COURS' ,'TERMINER', 'ARCHIVER']
    projet = Projet.objects.get(pk=pk)
    context = {'projet': projet, 'status': status[projet.status-1], 'pk': pk}
    template = loader.get_template('detailProjet.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def List_Intervenant_Project(request, pk):
    status = ['NON DÉBUTÉ', 'EN COURS' ,'TERMINER', 'ARCHIVER']
    projet = Projet.objects.get(pk=pk)
    intervenant = []
    intervenant.append(Projet.chef_project)
    intervenant.append(Projet.conducteur_travaux)
    intervenant.append(Projet.list_intervenant)
    print("inet:",intervenant)
    context = {
                'projet': projet,
                'status': status[projet.status-1],
                'pk': pk,
                'intervenant': intervenant
              }
    template = loader.get_template('intervenantProjet.html')
    return HttpResponse(template.render(context, request))
