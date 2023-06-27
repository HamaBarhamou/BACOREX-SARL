from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 
                  'list_materiels', 'budget', 'attribuer_a', 'projet', 'pieces_jointes']
