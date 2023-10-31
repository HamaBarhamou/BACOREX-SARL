from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime, timedelta,date
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from .forms import ClientForm, ProjetForm, TaskForm, TaskLimitedForm, PhaseForm
from .models import Client, Projet, Task, Phase
from plannig.models import Event
from .serializers import TaskSerializer
from django.views.decorators.http import require_POST
import pandas as pd
from openpyxl import Workbook
from django.db.models import F
from userprofile.models import User
from django.db.models import Prefetch
from django.db.models import Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
    
    for projet in projets:
        start_date = projet['start_date']
        end_date = projet['end_date']

        if date.today() < start_date:
            days_until_start = (start_date - date.today()).days
            projet['days_remaining'] = f"Commence dans {days_until_start} jours"
        else:
            days_remaining = (end_date - date.today()).days
            projet['days_remaining'] = f"{days_remaining if days_remaining > 0 else 'Terminé'} jours restants"


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


# vues pour la gestion des phases du projet

def list_phases_for_project(request, project_id):
    print('projetid=', project_id)
    projet = Projet.objects.get(pk=project_id)
    phases = Phase.objects.filter(projet_id=project_id)
    context = {'projet': projet, 'phases': phases,'pk':project_id, 'form':PhaseForm(), 'is_editing': False}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))

def new_phase_for_project(request, project_id):
    if request.method == 'POST':
        print('creation')
        form = PhaseForm(request.POST)
        if form.is_valid():
            phase = form.save(commit=False)
            phase.projet_id = project_id
            phase.save()
            return redirect('projectmanagement:list_phases_for_project', project_id=project_id)
    else:
        form = PhaseForm()
    context = {'form': form, 'project_id': project_id}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))

def phase_detail(request, phase_id, projet_id):
    phase = get_object_or_404(Phase, id=phase_id)
    context = {'phase': phase, 'pk':projet_id}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))

def edit_phase(request, phase_id, projet_id):
    phase = get_object_or_404(Phase, id=phase_id)
    if request.method == 'POST':
        print('requette poste')
        form = PhaseForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()
            #return redirect('projectmanagement:phase_detail', phase_id=phase.id, projet_id=projet_id)
            return redirect('projectmanagement:list_phases_for_project', project_id=projet_id)
    else:
        form = PhaseForm(instance=phase)
        #print(" vue de odification GET phase_id={} && projet_id={}".format(phase_id, projet_id))
    context = {'form': form, 'pk':projet_id, 'is_editing': True, 'phase': phase}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))

@require_POST
def delete_phase(request, phase_id, projet_id):
    print('suppression e')
    phase = get_object_or_404(Phase, id=phase_id)
    phase.delete()
    return redirect('projectmanagement:list_phases_for_project', project_id=projet_id)


# vue pour la revue protefeuille

def fetch_filtered_projet(search_term, start_date, end_date):
    print("Termes de recherche:", search_term, start_date, end_date)
    projets = Projet.objects.prefetch_related(
        'list_intervenant',
        'list_materiels',
        'coordinateur',
        'chef_project',
        'conducteur_travaux',
        'client'
    ).filter(
        Q(name__icontains=search_term) |
        Q(description__icontains=search_term) |
        Q(coordinateur__username__icontains=search_term) |
        Q(chef_project__username__icontains=search_term) |
        Q(conducteur_travaux__username__icontains=search_term) |
        Q(list_intervenant__username__icontains=search_term)
    )

    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        projets = projets.filter(start_date__gte=start_date_obj)

    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        projets = projets.filter(end_date__lte=end_date_obj)

    return projets.distinct()

def display_projet_data(request):
    search_term = request.GET.get('search_term', '')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    projets = fetch_filtered_projet(search_term, start_date, end_date)
    
    # Ajoutez ces lignes pour la pagination
    paginator = Paginator(projets, 10) # Afficher 10 projets par page
    page = request.GET.get('page')
    try:
        projets = paginator.page(page)
    except PageNotAnInteger:
        projets = paginator.page(1)
    except EmptyPage:
        projets = paginator.page(paginator.num_pages)

    for projet in projets:
        #print("p u: ",projet)
        projet.status_display = dict(projet.STATUS)[projet.status]
        projet.users = [
            projet.coordinateur.username,
            projet.chef_project.username,
            projet.conducteur_travaux.username
        ] + [user.username for user in projet.list_intervenant.all()]

    return render(request, 'revuePortefeuille.html', {
        'projets': projets,
        'search_term': search_term, 
        'start_date': start_date, 
        'end_date': end_date
    })
    #return render(request, 'revuePortefeuille.html', {'projets': projets, 'search_term': search_term, 'start_date': start_date, 'end_date': end_date})

def download_projet_data(request):
    search_term = request.GET.get('search_term', '')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    projets = fetch_filtered_projet(search_term, start_date, end_date)
    
    data = []

    for projet in projets:
        #print("p d: ",projet)
        users = [
            projet.coordinateur.username,
            projet.chef_project.username,
            projet.conducteur_travaux.username
        ]
        users.extend([user.username for user in projet.list_intervenant.all()])
        users_str = ', '.join(users)

        data.append({
            'Nom Projet': projet.name,
            'Description Projet': projet.description,
            'Intervenants': users_str,
            'Materiels': ', '.join([materiel.name for materiel in projet.list_materiels.all()]),
            'Client': projet.client.name,
            'Statut Projet': dict(projet.STATUS).get(projet.status),
            'Budget Projet': projet.budget,
            'Date de demarrage': projet.start_date,
            'Date de fin': projet.end_date,
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="revue_portefeuille.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Détails Projets')

    return response


def get_user_projects():
    users = User.objects.all()

    user_projects = {}

    for user in users:
        projects = set()  # Utilisez un ensemble pour éviter les doublons

        # Cherchez tous les rôles possibles pour l'utilisateur et ajoutez les projets correspondants à l'ensemble
        projects.update(user.cordinateur_projet.all())
        projects.update(user.chef_project.all())
        projects.update(user.conducteur_travaux.all())
        projects.update(user.intervenant.all())

        user_projects[user.username] = projects

    return user_projects
