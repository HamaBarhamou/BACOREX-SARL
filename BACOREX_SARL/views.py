from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect
from django.template import loader


@login_required(login_url="/user/")
def home(request):
    # if request.user.groups.filter(name="PROJET_TEAM").exists():
    if request.user.taskliste_redirection():
        return redirect("projectmanagement:taskliste")
    template = loader.get_template("home.html")
    context = {}
    return HttpResponse(template.render(context, request))


def notifications(request):
    template = loader.get_template("notifications.html")
    context = {}
    return HttpResponse(template.render(context, request))
