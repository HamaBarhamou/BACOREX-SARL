from django.db import models
from userprofile.models import User
from django.contrib.postgres.fields import JSONField
import json


class ActionHistory(models.Model):
    # Un identifiant unique pour l'entrée de l'historique sera créé automatiquement (id)

    # Qui a effectué l'action
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur', related_name='actions')

    # Type d'action effectuée (création, mise à jour, suppression)
    action_type = models.CharField("Type d'Action", max_length=50)

    # Sur quel type d'objet l'action a été effectuée (projet, tâche, utilisateur)
    entity_type = models.CharField("Type d'Entité", max_length=50)

    # Identifiant de l'entité concernée
    entity_id = models.PositiveIntegerField("ID de l'Entité")

    # Description détaillée ou données sérialisées des changements
    # Utilisez le JSONField intégré de Django
    action_details = models.JSONField("Détails de l'Action", blank=True, null=True)

    # Date et heure à laquelle l'action a été effectuée
    timestamp = models.DateTimeField("Horodatage", auto_now_add=True)

    class Meta:
        verbose_name = "Historique d'Action"
        verbose_name_plural = "Historiques d'Action"
        ordering = ['-timestamp']  # Ordonner par horodatage, les plus récents d'abord

    def __str__(self):
        return f"{self.user.username} a effectué {self.action_type} sur {self.entity_type} (ID: {self.entity_id}) - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def parse_detail(self, key, old_value, new_value):
        if isinstance(old_value, list) and isinstance(new_value, list):
            return f"{key} mis à jour avec {len(new_value)} élément(s)."
        elif isinstance(old_value, dict) and isinstance(new_value, dict):
            changes = [f"{k} changé de {v} à {new_value[k]}" for k, v in old_value.items() if v != new_value[k]]
            return f"{key}: " + ', '.join(changes) + "."
        else:
            return f"{key} changé de {old_value} à {new_value}."
    
    def details_as_story(self):
        details = self.action_details
        if not details:
            return "Détails non disponibles en format lisible."

        if 'Création' in self.action_type and not details.get('old_data'):
            # Si c'est une création, il n'y aura pas de données anciennes (old_data)
            if 'Création' in self.action_type and not details.get('old_data'):
                # Récupérer la valeur du champ 'name' depuis new_data, si disponible.
                entity_name = details.get('new_data', {}).get('name', 'Inconnu')
                return f"A creer une nouvelle {self.entity_type.lower()} (ID: {self.entity_id}) - nommée '{entity_name}'."


        # La logique actuelle pour les mises à jour ou les suppressions
        story_parts = []
        if 'old_data' in details and 'new_data' in details:
            for key, value in details['new_data'].items():
                old_value = details['old_data'].get(key, None)
                # Ajoutez seulement au récit si la valeur a changé
                if old_value != value:
                    story_parts.append(self.parse_detail(key, old_value, value))
        return ' '.join(story_parts)

    def action_summary(self):
        return f"{self.user.username} a effectué l'action '{self.action_type}' sur {self.entity_type.lower()} (ID: {self.entity_id}) à {self.timestamp.strftime('%H:%M')}."

