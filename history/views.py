from django.shortcuts import render
from .models import ActionHistory

def history_list(request):
    # Récupérez tous les objets historiques triés par timestamp
    histories = ActionHistory.objects.all().order_by('-timestamp')
    # Renvoyer ces objets au template
    return render(request, 'history_list.html', {'histories': histories})
