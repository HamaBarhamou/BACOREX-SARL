from django.apps import AppConfig


class GestionprojetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gestionprojets"

    def ready(self):
        import gestionprojets.signals  # noqa
