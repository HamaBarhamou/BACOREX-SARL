from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MessageForm
from django.template import loader
from userprofile.forms import LoginForm

# Create your views here.
def messagerie(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            messages = form.cleaned_data["messages"]
            recepteur = form.cleaned_data["recepteur"]
            date_envoie = form.cleaned_data["date_envoie"]
            status_envoie = form.cleaned_data["status_envoie"]
            

            # Renseigner l'itulisateur emetteur avant de sauvegarder
            #form.save()
            
        
    else:
        form = MessageForm()

    context = {'form':form}
    template = loader.get_template('message.html')
    return HttpResponse(template.render(context, request))