# Dans admin.py
from django.contrib import admin

from .models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ["id", "tva_pourcentage"]

    def has_add_permission(self, request):
        # N'autoriser qu'une seule entrée de configuration
        return not Configuration.objects.exists()
