from django.shortcuts import render
from .models import ActionHistory
from django.core.paginator import Paginator

def history_list(request):
    histories_list = ActionHistory.objects.all().order_by('-timestamp')
    paginator = Paginator(histories_list, 20)  # Afficher 10 historiques par page

    page_number = request.GET.get('page')
    histories = paginator.get_page(page_number)

    return render(request, 'history_list.html', {'histories': histories})

""" def history_list(request):
    # Récupérez tous les objets historiques triés par timestamp
    histories = ActionHistory.objects.all().order_by('-timestamp')
    # Renvoyer ces objets au template
    return render(request, 'history_list.html', {'histories': histories}) """
