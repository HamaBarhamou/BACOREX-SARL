from django.shortcuts import render
from django.http import HttpResponse
from .forms import DaoForm
from django.template import loader
from .models import DAO
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user/')
def home_dao(request):
    dao = DAO.objects.all().values()
    context = {
    'dao': dao,
    }
    template = loader.get_template('home_dao.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/user/')
def add_dao(request):
    if request.method == 'POST':
        form = DaoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DaoForm()

    context = {'form':form}
    template = loader.get_template('add_dao.html')
    return HttpResponse(template.render(context, request))