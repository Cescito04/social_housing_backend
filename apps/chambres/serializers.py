from rest_framework import serializers
from .models import Chambre
from apps.maisons.serializers import MaisonSerializer

class ChambreSerializer(serializers.ModelSerializer):
    maison = MaisonSerializer(read_only=True)

    class Meta:
        model = Chambre
        fields = [
            'id', 'maison', 'titre', 'description', 'taille', 'type',
            'meublee', 'salle_de_bain', 'prix', 'disponible', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 