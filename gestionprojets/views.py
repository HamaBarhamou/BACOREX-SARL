from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from .forms import ClientForm, ProjetForm, TaskForm, TaskLimitedForm
from .models import Client, Projet, Task
from plannig.models import Event
from .serializers import TaskSerializer

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
            return redirect('projectmanagement:clientlist') 
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
            return redirect('projectmanagement:projectlist')
    else:
        form = ProjetForm(instance=projet)
        context = {'form': form, 'pk': projet.pk}
        template = loader.get_template('editProjet.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def deletteProjet(request, pk):
    Projet.objects.get(pk=pk).delete()
    return redirect('gestionprojets:listeproject')


@login_required(login_url='/user/')
def listeProject(request):
    Directeur_Generale = 4
    Admin = 5
    Coordinateur_des_Operations = 6
    Conducteurs_des_Travaux = 7
    Chef_de_Projet = 8
    Intervenant = 11

    leader = [Directeur_Generale, Admin, Coordinateur_des_Operations]
    projets = []  # Définir projets comme une liste vide par défaut
    if request.user.fonction in leader or request.user.is_superuser:
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
    temps_restant = None
    if projet.status == 2:  # Assumons que 2 signifie 'EN COURS'
        temps_restant = (projet.end_date - datetime.now()).days
    context = {'projet': projet, 'status': status[projet.status], 'temps_restant': temps_restant, 'pk': pk}
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
    projet = get_object_or_404(Projet, pk=pk)
    #tasks = projet.task_set.all()  # Récupérer toutes les tâches associées à ce projet
    if request.user.is_chefDeProjet_or_coordinateur_or_admin():
        print("newTask TaskForm selected")
        tasks = projet.task_set.all()  # Récupérer toutes les tâches associées à ce projet
        form_class = TaskForm
    else:
        print("newTask InterventionForm selected")
        tasks = projet.task_set.filter(attribuer_a=request.user)  # Récupérer seulement les tâches attribuées à cet utilisateur
        form_class = TaskLimitedForm
    
    if request.method == "POST":
        #form = TaskForm(request.POST, request.FILES)
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.projet = projet  # Associer cette tâche au projet actuel
            try:
                task.full_clean() # Ajoutez cette ligne pour appeler explicitement la méthode clean du modèle
            except ValidationError as e:
                form.add_error(None, e)
            else:
                task.save()
                form.save_m2m()  # Important lorsque vous avez des champs ManyToMany
                #form = TaskForm()
                form = form_class()
        else:
            #form = TaskForm(request.POST, request.FILES)
            form = form_class(request.POST, request.FILES)
    else:
        #form = TaskForm()
        form = form_class()
   
    context = {'form': form, 'pk': pk, 'tasks': tasks, 'projet': projet}
    template = loader.get_template('newTask.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def editTask(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.is_chefDeProjet_or_coordinateur_or_admin():
        print("editTask TaskForm selected")
        form_class = TaskForm
    else:
        print("editTask InterventionForm selected")
        form_class = TaskLimitedForm

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == "POST":
            form = form_class(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.save()  # Sauvegardez les données
                updated_task = Task.objects.get(pk=pk)  # Récupérez l'objet mis à jour de la base de données
                serializer = TaskSerializer(updated_task)  # Sérialisez les données mises à jour
                # Retournez une réponse JSON avec les données mises à jour
                return JsonResponse({'status': 'success', 'message': 'Tâche modifiée avec succès', 'updated_task': serializer.data}, status=200)
            else:
                # retourner une réponse JSON en cas d'échec de la validation du formulaire
                print(form.errors)

                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        else:
            serializer = TaskSerializer(task)
            return JsonResponse(serializer.data)
    else:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('projectmanagement:detailprojet', args=(task.projet.pk,)))
        else:
            return HttpResponseRedirect(reverse('projectmanagement:detailprojet', args=(task.projet.pk,)))


@login_required(login_url='/user/')
def deleteTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    projet_pk = task.projet.pk  # Sauvegarde le pk du projet pour la redirection
    task.delete()
    return redirect('projectmanagement:newTask', pk=projet_pk)



    
   
