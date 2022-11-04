from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import ConnexionForm
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect


# Create your views here.
def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = True
    else:
        form = ConnexionForm()

    context = {
        'error':error,
        'form':form
    }
    
    template = loader.get_template('connexion.html')
    #return render(request, 'connexion.html', locals())
    return HttpResponse(template.render(context, request))

def logout(request):
    logout(request)