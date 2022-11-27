from django.shortcuts import render, HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required



@login_required(login_url='/user/')
def home(request):
    template = loader.get_template('home.html')
    context={}
    return HttpResponse(template.render(context,request))