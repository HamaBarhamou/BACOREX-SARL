from django.shortcuts import render
from .models import ActionHistory
from django.core.paginator import Paginator

def history_list(request):
    histories_list = ActionHistory.objects.all().order_by('-timestamp')
    paginator = Paginator(histories_list, 15)  # Afficher 10 historiques par page

    page_number = request.GET.get('page')
    histories = paginator.get_page(page_number)

    return render(request, 'history_list.html', {'histories': histories})

