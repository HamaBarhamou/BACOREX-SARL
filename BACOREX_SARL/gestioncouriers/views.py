from django.shortcuts import render
from django.http import HttpResponse
from .forms import MessageForm
from django.template import loader

# Create your views here.
def messagerie(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MessageForm()

    context = {'form':form}
    template = loader.get_template('message.html')
    return HttpResponse(template.render(context, request))