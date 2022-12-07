from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/user/')
def magasin_home(request):
    context = {}
    template = loader.get_template('magasin.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/user/')
def categorie_home(request):
    context = {}
    template = loader.get_template('magasin.html')
    return HttpResponse(template.render(context, request))