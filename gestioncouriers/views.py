from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import MessageForm
from django.template import loader
from userprofile.forms import LoginForm
from .models import Message, Document, MessagePredefini
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from gestioncouriers.utils import send_notification_email
from django.shortcuts import get_object_or_404
from gestionprojets.models import Projet



# Create your views here.
""" @login_required(login_url='/user/')
def messagerie(request, projet_id=None):
    projet = None
    context = {}
    if projet_id:
        projet = get_object_or_404(Projet, pk=projet_id)
        context['projet_id'] = projet_id
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            objet = form.cleaned_data["objet"]
            messages = form.cleaned_data["messages"]
            message_predefini = form.cleaned_data.get("message_predefini")

            msg = Message(
                objet=objet,
                messages=messages,
                emetteur=request.user,
                date_envoie=datetime.datetime.now(datetime.timezone.utc),
                status_envoie=True,
                projet = projet
            )
            msg.save()

            if message_predefini:
                recepteur = projet.get_user_by_role_name(message_predefini.destinataire_role)
                msg.recepteurs.add(recepteur)
            else:
                recepteurs = form.cleaned_data["recepteurs"]
                for user in recepteurs:
                    msg.recepteurs.add(user)
                    #send_notification_email(user, objet)
                
            form = MessageForm(user=request.user, projet=projet) 
            if 'message_predefini' in form.cleaned_data and form.cleaned_data['message_predefini']:
                form.update_messages_field(form.cleaned_data['message_predefini'].id)
                # Ici, vous pouvez ajuster le traitement du message en fonction du message prédéfini choisi
    else:
        form = MessageForm(user=request.user, projet=projet) 
    context['form'] = form
    template = loader.get_template('message.html')
    return HttpResponse(template.render(context, request)) """

@login_required(login_url='/user/')
def messagerie(request, projet_id=None):
    projet = None
    context = {}
    if projet_id:
        projet = get_object_or_404(Projet, pk=projet_id)
        context['projet_id'] = projet_id 
        context['projet'] = projet 
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user, projet=projet)
        if form.is_valid():
            objet = form.cleaned_data["objet"]
            messages = form.cleaned_data["messages"]
            message_predefini = form.cleaned_data.get("message_predefini")
            msg = Message(
                objet=objet,
                messages=messages,
                emetteur=request.user,
                date_envoie=datetime.datetime.now(datetime.timezone.utc),
                status_envoie=True,
                projet=projet
            )
            msg.save()
            if message_predefini:
                role_user = projet.get_user_by_type_choice(message_predefini.destinataire_role)
                recepteur = projet.get_user_by_role_name(role_user)
                if recepteur is not None:
                    msg.recepteurs.add(recepteur)
            else:
                recepteurs = form.cleaned_data["recepteurs"]
                for user in recepteurs:
                    msg.recepteurs.add(user)
                    #send_notification_email(user, objet)
            form = MessageForm(user=request.user, projet=projet)
            if message_predefini:
                form.update_messages_field(message_predefini.id)
    else:
        form = MessageForm(user=request.user, projet=projet) 
    context['form'] = form
    template = loader.get_template('message.html')
    return HttpResponse(template.render(context, request))



@login_required(login_url='/user/')
def boitemessagerie(request, projet_id=None):
    projet = get_object_or_404(Projet, pk=projet_id)
    context = {'projet_id':projet_id, 'projet':projet}
    template = loader.get_template('messagerie.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def courier_entrant(request, projet_id=None):
    context = {}
    if projet_id:
        projet = get_object_or_404(Projet, pk=projet_id)
        context['projet_id'] = projet_id
        context['projet'] = projet
        messages = Message.objects.filter(recepteurs=request.user, projet=projet).order_by('-date_envoie')
    else:
        messages = Message.objects.filter(recepteurs=request.user).order_by('-date_envoie')
    #context = {'messages': messages}
    context['messages'] = messages
    template = loader.get_template('courier_entrant.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def courier_envoye(request, projet_id=None):
    context = {}
    if projet_id:
        # Si un projet est spécifié, ne montrer que les messages liés à ce projet
        projet = get_object_or_404(Projet, pk=projet_id)
        messages_envoyes = Message.objects.filter(emetteur=request.user, projet=projet).order_by('-date_envoie')
        context['projet_id'] = projet_id
        context['projet'] = projet
    else:
        # Sinon, montrer tous les messages envoyés par l'utilisateur
        messages_envoyes = Message.objects.filter(emetteur=request.user).order_by('-date_envoie')
    context['messages'] = messages_envoyes
    return render(request, 'courier_envoye.html', context)


@login_required(login_url='/user/')
def detail_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    return render(request, 'detail_message.html', {'message': message})


@login_required(login_url='/user/')
def reply_to_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    projet = original_message.projet
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            new_message = Message()
            new_message.objet = form.cleaned_data.get('objet')
            new_message.messages = form.cleaned_data.get('messages')
            new_message.emetteur = request.user
            new_message.status_envoie = True
            new_message.projet = projet
            new_message.fil_de_discussion = original_message
            new_message.save()
            new_message.recepteurs.add(original_message.emetteur)
            for f in request.FILES.getlist('documents'):
                doc = Document(file=f)
                doc.save()
                new_message.documents.add(doc)
            new_message.save()
            send_notification_email(
                new_message.recepteurs.all(),
                new_message.objet,
                new_message.messages
            )
            return redirect('mailmanagement:messagerie')
    else:
        form = MessageForm(initial={
            'objet': 'Re: ' + original_message.objet,
            'recepteurs': [original_message.emetteur.id]
        }, user=request.user)
    return render(request, 'reply.html', {'form': form, 'original_message': original_message})


def get_predefined_message(request, message_id):
    message_predefini = get_object_or_404(MessagePredefini, pk=message_id)
    data = {
        'titre': message_predefini.titre,
        'corps': message_predefini.corps,
        'expeditaire_role': message_predefini.expeditaire_role,
        'destinataire_role': message_predefini.destinataire_role
    }
    return JsonResponse(data)
