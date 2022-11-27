from django.shortcuts import render, HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('home.html')
    context={}
    return HttpResponse(template.render(context,request))