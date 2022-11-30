from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MessageForm
from django.template import loader
from userprofile.forms import LoginForm
from .models import Message
import datetime
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url='/user/')
def messagerie(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            objet = form.cleaned_data["objet"]
            messages = form.cleaned_data["messages"]
            recepteur = form.cleaned_data["recepteur"]
            msg = Message(objet = objet,
                          messages = messages,
                          emetteur = request.user,
                          recepteur = recepteur,
                          date_envoie = datetime.datetime.now(datetime.timezone.utc),
                          status_envoie = True
                          )
            msg.save()
            form = MessageForm()
    else:
        form = MessageForm()
        #form.changed_data

    context = {'form':form}
    template = loader.get_template('message.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def boitemessagerie(request):
    context = {}
    template = loader.get_template('messagerie.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def courier_entrant(request):
    q = Message.objects.all()
    context = {'message': q}
    template = loader.get_template('courier_entrant.html')
    return HttpResponse(template.render(context, request))