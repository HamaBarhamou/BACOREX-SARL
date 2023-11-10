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
            changes = [f"{k} a changé de '<b>{v}</b>' à '<b>{new_value[k]}</b>'" for k, v in old_value.items() if v != new_value[k]]
            return f"{key}: " + ', '.join(changes) + "."
        else:
            return f"{key} a changé de '<b>{old_value}</b>' à '<b>{new_value}</b>'."

    
    def details_as_story(self):
        details = self.action_details
        if not details:
            return "Détails non disponibles en format lisible."

        entity_name = details.get('new_data', {}).get('name', details.get('old_data', {}).get('name', 'Inconnu'))

        # Pour une création, affichez simplement le nom de l'entité créée.
        if 'Création' in self.action_type and not details.get('old_data'):
            #entity_name = details.get('new_data', {}).get('name', 'Inconnu')
            return f"A créé une nouvelle {self.entity_type.lower()} (ID: {self.entity_id}) - '{entity_name}'."

        # Pour une suppression, affichez le nom de l'entité supprimée.
        if 'Suppression' in self.action_type:
            #entity_name = details.get('old_data', {}).get('name', 'Inconnu')
            return f"A supprimé {self.entity_type.lower()} (ID: {self.entity_id}) - '{entity_name}'."

        # Pour une mise à jour, introduisez la narration avec l'action et l'ID.
        if 'Modification' in self.action_type:
            story_parts = [f"<strong>A modifier {self.entity_type.lower()} (ID: {self.entity_id}): {entity_name}</strong>"]

            if 'old_data' in details and 'new_data' in details:
                for key, value in details['new_data'].items():
                    old_value = details['old_data'].get(key, None)
                    if old_value != value:
                        change = self.parse_detail(key, old_value, value)
                        story_parts.append(f"<span class='text-change'>{change}</span>")

            return ' '.join(story_parts)

        # Si on a seulement des 'old_data', c'est une suppression.
        if 'old_data' in details and 'new_data' not in details:
            for key, old_value in details['old_data'].items():
                story_parts.append(f"{key} supprimé (était '{old_value}').")

        return ' '.join(story_parts)
    


    def action_summary(self):
        return f"{self.user.username} a effectué l'action '{self.action_type}' sur {self.entity_type.lower()} (ID: {self.entity_id}) à {self.timestamp.strftime('%H:%M')}."

