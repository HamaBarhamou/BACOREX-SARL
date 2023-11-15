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
from .forms import ClientForm, ProjetForm, TaskForm, TaskLimitedForm, PhaseForm, AgentForm
from .models import Client, Projet, Task, Phase
from plannig.models import Event
from .serializers import TaskSerializer, PhaseSerializer, ProjetSerializer, ClientSerializer
from django.views.decorators.http import require_POST
import pandas as pd
from openpyxl import Workbook
from django.db.models import F
from userprofile.models import User
from django.db.models import Prefetch
from django.db.models import Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from history.models import ActionHistory
import json



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

@login_required(login_url='/user/')
def ganttchartprojects(request):
    projets = Projet.objects.all().order_by('end_date', 'start_date')
    # Création des labels et des données pour le graphique de Gantt
    gantt_labels = []
    gantt_data = []

    status_colors = {  # Couleurs selon le statut du projet
        1: 'gray',   # NON DÉBUTÉ
        2: 'blue',   # EN COURS
        3: 'green',  # TERMINÉ
        4: 'red',    # ARCHIVÉ
    }

    # Parcourir toutes les tâches et construire les données pour le graphique de Gantt
    for projet in projets:
        percent_done = projet.pourcentage_achevement()
        # Construction du tooltip
        tooltip = f"Coordinateur: {projet.coordinateur.get_full_name()}, "\
                  f"Chef de projet: {projet.chef_project.get_full_name()}, "\
                  f"Conducteur de travaux: {projet.conducteur_travaux.get_full_name()}"
        
        print('tooltip=',tooltip)
        
        gantt_labels.append(projet.name)
        gantt_data.append({
            'id': projet.id,
            'name': projet.name,
            'start': projet.start_date.strftime("%Y-%m-%d"),  # Format pour correspondre à l'attente JS
            'end': projet.end_date.strftime("%Y-%m-%d"),
            'status': projet.status,
            'percentDone': percent_done,
            'color': status_colors[projet.status],
            'tooltip': tooltip,
        })
    
    context = {
        'gantt_labels': gantt_labels,  # Utilisés pour les labels sur l'axe des ordonnées
        'gantt_data': gantt_data,
    }
    #print('context=',context)
    return render(request, 'ganttchartprojects.html', context)


@login_required(login_url='/user/')
def Taskliste(request):
    # Récupérer toutes les tâches pour l'utilisateur connecté
    user_tasks = Task.objects.filter(attribuer_a__in=[request.user]).prefetch_related('attribuer_a').order_by('end_date', 'start_date')

    # Création des labels et des données pour le graphique de Gantt
    gantt_labels = []
    gantt_data = []

    # Parcourir toutes les tâches et construire les données pour le graphique de Gantt
    for task in user_tasks:
        # Déterminer le pourcentage achevé de la tâche
        if task.status == 3:  # Si la tâche est terminée
            percent_done = 100
        elif task.status == 1:  # Si la tâche n'a pas commencé
            percent_done = 0
        elif task.status == 2:  # Si la tâche est en cours
            total_days = (task.end_date - task.start_date).days
            days_passed = (date.today() - task.start_date).days
            percent_done = (days_passed / total_days) * 100 if total_days > 0 else 0
            percent_done = min(max(percent_done, 0), 100)  # S'assurer que le pourcentage reste entre 0 et 100

        gantt_labels.append(task.name)
        gantt_data.append({
            'name': task.name,
            'start': task.start_date.strftime("%Y-%m-%d"),  # Format pour correspondre à l'attente JS
            'end': task.end_date.strftime("%Y-%m-%d"),
            'status': task.status,
            'percentDone': percent_done,
        })

    # Séparer les tâches en cours, à venir, expirées et terminées 
    not_started_tasks = user_tasks.filter(start_date__lte=date.today(),end_date__gte=date.today(),status=1)
    ongoing_tasks = user_tasks.filter(start_date__lte=date.today(), end_date__gte=date.today(), status=2)
    upcoming_tasks = user_tasks.filter(start_date__gt=date.today())
    expired_tasks = user_tasks.filter(end_date__lt=date.today(), status__in=[1, 2])  # Supposons que le statut 3 est pour "Terminé"
    completed_tasks = user_tasks.filter(status=3)

    # Pour les autres tâches (non assignées à l'utilisateur)
    other_tasks = Task.objects.exclude(attribuer_a__in=[request.user]).prefetch_related('attribuer_a').order_by('end_date', 'start_date')

    context = {
        'not_started_tasks': not_started_tasks,
        'ongoing_tasks': ongoing_tasks,
        'upcoming_tasks': upcoming_tasks,
        'expired_tasks': expired_tasks,
        'completed_tasks': completed_tasks,
        'other_tasks': other_tasks,
        'to_days':date.today(),
        'gantt_labels': gantt_labels,  # Utilisés pour les labels sur l'axe des ordonnées
        'gantt_data': gantt_data,
    }

    return render(request, 'listeTask.html', context)


# Create your views here.
@login_required(login_url='/user/')
def newClient(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            client_id = client.id
            new_data = ClientSerializer(client).data
            ActionHistory.objects.create(
                user=request.user,
                action_type='Création de Client',
                entity_type='Client',
                entity_id=client_id,
                action_details={
                    'old_data': {},
                    'new_data': new_data
                }
            )
            return redirect('projectmanagement:clientlist') 
    else:
        form = ClientForm()
        context = {'form': form}
        template = loader.get_template('newclient.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def listeClient(request):
    # Récupération du terme de recherche
    search_term = request.GET.get('search_term', '')
    clients_list = Client.objects.prefetch_related('projet_set').all()

    # Filtrage en fonction du terme de recherche
    if search_term:
        clients_list = clients_list.filter(
            Q(name__icontains=search_term) | Q(adresse__icontains=search_term)
        )

    # Pagination
    paginator = Paginator(clients_list, 10)  # Afficher 10 clients par page
    page = request.GET.get('page')
    clients = paginator.get_page(page)

    context = {
        'clients': clients,
        'search_term': search_term
    }
    return render(request, 'listeclient.html', context)


@login_required(login_url='/user/')
def newProjet(request):
    if request.method == "POST":
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save()
            ActionHistory.objects.create(
                user=request.user,
                action_type='Création de projet',
                entity_type='Projet',
                entity_id=projet.id,
                action_details={
                    'old_data': {},
                    'new_data': ProjetSerializer(projet).data
                }
            )
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
        old_data = ProjetSerializer(projet).data
        if form.is_valid():
            projet = form.save()
            new_data = ProjetSerializer(projet).data
            ActionHistory.objects.create(
                user=request.user,
                action_type='Modification de projet',
                entity_type='Projet',
                entity_id=projet.id,
                action_details={
                    'old_data': old_data,
                    'new_data': new_data
                }
            )
            return redirect('projectmanagement:projectlist')
    else:
        form = ProjetForm(instance=projet)
        context = {'form': form, 'pk': projet.pk}
        template = loader.get_template('editProjet.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def deletteProjet(request, pk):
    #Projet.objects.get(pk=pk).delete()
    projet = Projet.objects.get(pk=pk)
    projet_id = projet.id
    old_data = ProjetSerializer(projet).data
    projet.delete()
    ActionHistory.objects.create(
        user=request.user,
        action_type = 'Suppression de projet',
        entity_type = 'Projet',
        entity_id = projet_id,
        action_details = {
            'old_data': old_data,
            'new_data': {}
        }
    )
    return redirect('projectmanagement:projectlist')

@login_required(login_url='/user/')
def listeProject(request):
    query = request.GET.get('q')
    projets_list = Projet.get_projects_by_user(request.user)
    if query:
        projets_list = projets_list.filter(name__icontains=query)  # Recherche par nom de projet
    page = request.GET.get('page', 1)
    paginator = Paginator(projets_list, 10)  # 10 projets par page

    try:
        projets = paginator.page(page)
    except PageNotAnInteger:
        projets = paginator.page(1)
    except EmptyPage:
        projets = paginator.page(paginator.num_pages)

    context = {'projets': projets, 'query':query}

    return render(request, 'listeproject.html', context)


@login_required(login_url='/user/')
def detailProject(request, pk):
    #status = ['', 'NON DÉBUTÉ', 'EN COURS' ,'TERMINER', 'ARCHIVER']
    projet = Projet.objects.get(pk=pk)
    temps_restant = None
    if projet.status == 2:  # Assumons que 2 signifie 'EN COURS'
        temps_restant = (projet.end_date - datetime.now()).days
    context = {'projet': projet, 'status': projet.get_status_display(), 'temps_restant': temps_restant, 'pk': pk}
    template = loader.get_template('detailProjet.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def caracteristiques_techniques(request, pk):
    projet = Projet.objects.get(pk=pk)
    temps_restant = None
    if projet.status == 2:  # Assumons que 2 signifie 'EN COURS'
        temps_restant = (projet.end_date - datetime.now()).days
    context = {'projet': projet, 'status': projet.get_status_display(), 'temps_restant': temps_restant, 'pk': pk}
    template = loader.get_template('caracteristiques_techniques.html')
    return HttpResponse(template.render(context, request))




@login_required(login_url='/user/')
def manage_agents(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    users = User.objects.filter(groups__name='PROJET_TEAM')

    users_info = [
        {
            'user': user,
            'role': projet.get_user_role(user)
        }
        for user in users
    ]

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        if 'add' in request.POST:
            projet.list_intervenant.add(user)
        elif 'remove' in request.POST:
            projet.list_intervenant.remove(user)

        return redirect('projectmanagement:manage_agents', pk=projet.id)

    context = {
        'projet': projet,
        'users_info': users_info,
        'pk': pk,
        'status': projet.get_status_display()
    }

    return render(request, 'manage_agents.html', context)


@login_required(login_url='/user/')
def add_agent(request, project_id, user_id):
    projet = get_object_or_404(Projet, pk=project_id)
    user = get_object_or_404(User, pk=user_id)
    projet.list_intervenant.add(user)
    return redirect('projectmanagement:manage_agents', pk=projet.id)

@login_required(login_url='/user/')
def remove_agent(request, project_id, user_id):
    projet = get_object_or_404(Projet, pk=project_id)
    user = get_object_or_404(User, pk=user_id)
    projet.list_intervenant.remove(user)
    return redirect('projectmanagement:manage_agents', pk=projet.id)






@login_required(login_url='/user/')
def List_Intervenant_Project(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    intervenants = projet.get_all_users()
    # Créer une liste pour stocker les informations et le rôle de chaque utilisateur
    users_info = [
        {
            'user': user,
            'role': projet.get_user_role(user)
        }
        for user in intervenants
    ]
    
    context = {
                'projet': projet,
                'status': projet.get_status_display(),
                'pk': pk,
                'intervenant': intervenants,
                'users_info': users_info,
              }
    template = loader.get_template('intervenantProjet.html')
    return HttpResponse(template.render(context, request))


""" @login_required(login_url='/user/')
def newTask(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.user.is_chefDeProjet_or_coordinateur_or_admin():
        print("newTask TaskForm selected")
        tasks = projet.task_set.all()  # Récupérer toutes les tâches associées à ce projet
        form_class = TaskForm
        #form_class = TaskForm(projet=projet) 
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
                ActionHistory.objects.create(
                    user=request.user,
                    action_type='Création de tâche',
                    entity_type='Tâche',
                    entity_id=task.id,
                    action_details={
                        'old_data': {},
                        #'new_data': form.cleaned_data  # Les données après la création
                        'new_data': TaskSerializer(task).data
                    }
                )
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
    return HttpResponse(template.render(context, request)) """

@login_required(login_url='/user/')
def newTask(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    tasks = projet.task_set.all() if request.user.is_chefDeProjet_or_coordinateur_or_admin() else projet.task_set.filter(attribuer_a=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, projet=projet) if request.user.is_chefDeProjet_or_coordinateur_or_admin() else TaskLimitedForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.projet = projet
            try:
                task.full_clean()
            except ValidationError as e:
                form.add_error(None, e)
            else:
                task.save()
                form.save_m2m()
                ActionHistory.objects.create(
                    user=request.user,
                    action_type='Création de tâche',
                    entity_type='Tâche',
                    entity_id=task.id,
                    action_details={
                        'old_data': {},
                        'new_data': TaskSerializer(task).data
                    }
                )
                form = TaskForm(projet=projet) if request.user.is_chefDeProjet_or_coordinateur_or_admin() else TaskLimitedForm()
    else:
        form = TaskForm(projet=projet) if request.user.is_chefDeProjet_or_coordinateur_or_admin() else TaskLimitedForm()
   
    context = {'form': form, 'pk': pk, 'tasks': tasks, 'projet': projet}
    return render(request, 'newTask.html', context)



@login_required(login_url='/user/')
def editTask(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Choisissez le bon formulaire en fonction du rôle de l'utilisateur
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
                original_task = Task.objects.get(pk=pk)  # Conservez l'état original de la tâche pour l'historique
                form.save()  # Sauvegardez les modifications

                # Enregistrez l'action dans l'historique
                ActionHistory.objects.create(
                    user=request.user,
                    action_type='Modification',
                    entity_type='Tâche',
                    entity_id=task.pk,
                    action_details={
                        'old_data': TaskSerializer(original_task).data,
                        'new_data': TaskSerializer(task).data
                    }
                )

                # Récupérez l'objet mis à jour de la base de données
                updated_task = Task.objects.get(pk=pk)
                serializer = TaskSerializer(updated_task)
                return JsonResponse({'status': 'success', 'message': 'Tâche modifiée avec succès', 'updated_task': serializer.data}, status=200)
            else:
                print(form.errors)
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        else:
            serializer = TaskSerializer(task)
            return JsonResponse(serializer.data)

    else:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES, instance=task)
            if form.is_valid():
                original_task = Task.objects.get(pk=pk)  # Conservez l'état original de la tâche pour l'historique
                form.save()  # Sauvegardez les modifications

                # Enregistrez l'action dans l'historique
                ActionHistory.objects.create(
                    user=request.user,
                    action_type='Modification',
                    entity_type='Tâche',
                    entity_id=task.pk,
                    action_details={
                        'old_data': TaskSerializer(original_task).data,
                        'new_data': TaskSerializer(task).data
                    }
                )

                # Redirigez l'utilisateur vers la page de détail du projet
                return HttpResponseRedirect(reverse('projectmanagement:detailprojet', args=(task.projet.pk,)))

        # Si la méthode n'est pas POST, redirigez simplement l'utilisateur
        return HttpResponseRedirect(reverse('projectmanagement:detailprojet', args=(task.projet.pk,)))

@login_required(login_url='/user/')
def deleteTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    projet_pk = task.projet.pk  # Sauvegarde le pk du projet pour la redirection
    # Sauvegarde des données de la tâche pour l'historique
    old_data = TaskSerializer(task).data
    task_id = task.id 
    task.delete()
    # Création de l'historique avant la suppression
    ActionHistory.objects.create(
        user=request.user,
        action_type='Suppression',
        entity_type='Tâche',
        entity_id=task_id,
        action_details={
            'old_data': old_data,
            'new_data': {}
        }
    )
    return redirect('projectmanagement:newTask', pk=projet_pk)


# vues pour la gestion des phases du projet

@login_required(login_url='/user/')
def list_phases_for_project(request, project_id):
    print('projetid=', project_id)
    projet = Projet.objects.get(pk=project_id)
    phases = Phase.objects.filter(projet_id=project_id)
    context = {
        'projet': projet,
        'phases': phases,
        'pk':project_id,
        'form':PhaseForm(),
        'is_editing': False,
        'status': projet.get_status_display()
    }
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def new_phase_for_project(request, project_id):
    if request.method == 'POST':
        form = PhaseForm(request.POST)
        if form.is_valid():
            phase = form.save(commit=False)
            phase.projet_id = project_id
            phase.save()
            ActionHistory.objects.create(
                    user=request.user,
                    action_type='Création de phase',
                    entity_type='Phase',
                    entity_id=phase.id,
                    action_details={
                        'old_data': {},
                        'new_data': PhaseSerializer(phase).data
                    }
                )
            return redirect('projectmanagement:list_phases_for_project', project_id=project_id)
    else:
        form = PhaseForm()
    context = {'form': form, 'project_id': project_id}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def phase_detail(request, phase_id, projet_id):
    phase = get_object_or_404(Phase, id=phase_id)
    context = {'phase': phase, 'pk':projet_id}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def edit_phase(request, phase_id, projet_id):
    phase = get_object_or_404(Phase, id=phase_id)
    old_data = PhaseSerializer(phase).data 
    if request.method == 'POST':
        form = PhaseForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()
            new_data = PhaseSerializer(phase).data  # Données après modification
            ActionHistory.objects.create(
                    user=request.user,
                    action_type='Modification',
                    entity_type='Phase',
                    entity_id=phase.pk,
                    action_details={
                        'old_data': old_data,
                        'new_data': new_data
                    }
                )
            return redirect('projectmanagement:list_phases_for_project', project_id=projet_id)
    else:
        form = PhaseForm(instance=phase)
    context = {'form': form, 'pk':projet_id, 'is_editing': True, 'phase': phase}
    template = loader.get_template('plannification.html')
    return HttpResponse(template.render(context, request))


@require_POST
@login_required(login_url='/user/')
def delete_phase(request, phase_id, projet_id):
    phase = get_object_or_404(Phase, id=phase_id)
    old_data = PhaseSerializer(phase).data 
    phase_id = phase.id
    phase.delete()
    ActionHistory.objects.create(
        user=request.user,
        action_type='Suppression',
        entity_type='Phase',
        entity_id=phase_id,
        action_details={
            'old_data': old_data,
            'new_data': {}
        }
    )
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

    if start_date and start_date != 'None':
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        projets = projets.filter(start_date__gte=start_date_obj)

    if end_date and end_date != 'None':
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
        projet.users = [user.username for user in projet.get_all_users()]

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
        users = [user.username for user in projet.get_all_users()]
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


