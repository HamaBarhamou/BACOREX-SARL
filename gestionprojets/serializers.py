from rest_framework import serializers
from .models import Task,Phase
from gestiondesstock.serializers import MaterielsSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 
                  'list_materiels', 'budget', 'attribuer_a', 'projet', 'pieces_jointes']

""" class TaskSerializer(serializers.ModelSerializer):
    attribuer_a = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
     )
    list_materiels = MaterielsSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 
                  'list_materiels', 'budget', 'attribuer_a', 'projet', 'pieces_jointes'] """

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'projet']