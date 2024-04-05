from django.shortcuts import render


# Create your views here.
def all_notifications(request):
    return render(request, "all_notifications.html", {"notification": "notification"})
