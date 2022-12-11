from django.shortcuts import render, HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



@login_required(login_url='/user/')
def home(request):
    if request.user.groups.filter(name='PROJET_TEAM').exists():
        return redirect('/projet')
    template = loader.get_template('home.html')
    context={}
    return HttpResponse(template.render(context,request))