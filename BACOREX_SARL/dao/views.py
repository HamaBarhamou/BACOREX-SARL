from django.shortcuts import render
from django.http import HttpResponse
from .forms import DaoForm
from django.template import loader
from .models import DAO

def home_dao(request):
    dao = DAO.objects.all().values()
    context = {
    'dao': dao,
    }
    template = loader.get_template('home_dao.html')
    return HttpResponse(template.render(context, request))
    #render(request, 'dao/home_dao.html',{})

def add_dao(request):
    template = loader.get_template('add_dao.html')
    return HttpResponse(template.render({}, request))