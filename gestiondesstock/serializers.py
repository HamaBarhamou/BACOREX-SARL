from rest_framework import serializers
from .models import CategoriMateriel, Entrepot, Materiels


class CategoriMaterielSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriMateriel
        fields = ["id", "name", "description"]


class EntrepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepot
        fields = ["id", "name", "adresse"]


class MaterielsSerializer(serializers.ModelSerializer):
    categorie = CategoriMaterielSerializer(read_only=True)
    entrepot = EntrepotSerializer(read_only=True)

    class Meta:
        model = Materiels
        fields = ["id", "name", "description", "qte", "categorie", "entrepot", "image"]
        extra_kwargs = {"image": {"required": False, "allow_null": True}}
