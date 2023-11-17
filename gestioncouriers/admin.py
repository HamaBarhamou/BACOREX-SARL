from django.contrib import admin
from .models import MessagePredefini

@admin.register(MessagePredefini)
class MessagePredefiniAdmin(admin.ModelAdmin):
    list_display = ('titre', 'corps', 'expeditaire_role', 'destinataire_role')
    search_fields = ('titre', 'projet__nom')
