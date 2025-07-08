from rest_framework import serializers
from .models import Chambre
from apps.maisons.serializers import MaisonSerializer

class ChambreSerializer(serializers.ModelSerializer):
    maison = serializers.PrimaryKeyRelatedField(queryset=Chambre._meta.get_field('maison').related_model.objects.all(), write_only=True)
    maison_detail = MaisonSerializer(source='maison', read_only=True)

    class Meta:
        model = Chambre
        fields = [
            'id', 'maison', 'maison_detail', 'titre', 'description', 'taille', 'type',
            'meublee', 'salle_de_bain', 'prix', 'disponible', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 