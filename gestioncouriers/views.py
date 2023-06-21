from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MessageForm
from django.template import loader
from userprofile.forms import LoginForm
from .models import Message, Document
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from gestioncouriers.utils import send_notification_email
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required(login_url='/user/')
def messagerie(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            objet = form.cleaned_data["objet"]
            messages = form.cleaned_data["messages"]
            recepteurs = form.cleaned_data["recepteurs"]
            msg = Message(
                objet=objet,
                messages=messages,
                emetteur=request.user,
                date_envoie=datetime.datetime.now(datetime.timezone.utc),
                status_envoie=True
            )
            msg.save()
            for user in recepteurs:
                msg.recepteurs.add(user)
                send_notification_email(user, objet)
                
            form = MessageForm(user=request.user)
    else:
        form = MessageForm(user=request.user)
    context = {'form': form}
    template = loader.get_template('message.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def boitemessagerie(request):
    context = {}
    template = loader.get_template('messagerie.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def courier_entrant(request):
    q = Message.objects.filter(recepteurs=request.user).order_by('-date_envoie')
    context = {'message': q}
    template = loader.get_template('courier_entrant.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def courier_envoye(request):
    messages_envoyes = Message.objects.filter(emetteur=request.user).order_by('-date_envoie')
    return render(request, 'courier_envoye.html', {'messages': messages_envoyes})

@login_required(login_url='/user/')
def detail_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    return render(request, 'detail_message.html', {'message': message})

@login_required(login_url='/user/')
def reply_to_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            new_message = Message()
            new_message.objet = form.cleaned_data.get('objet')
            new_message.messages = form.cleaned_data.get('messages')
            new_message.emetteur = request.user
            new_message.status_envoie = True
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
        })
    return render(request, 'reply.html', {'form': form, 'original_message': original_message})

