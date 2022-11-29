from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MessageForm
from django.template import loader
from userprofile.forms import LoginForm
from .models import Message
import datetime

# Create your views here.
def messagerie(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            messages = form.cleaned_data["messages"]
            recepteur = form.cleaned_data["recepteur"]
            msg = Message(messages = messages,
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


def boitemessagerie(request):
    context = {}
    template = loader.get_template('messagerie.html')
    return HttpResponse(template.render(context, request))