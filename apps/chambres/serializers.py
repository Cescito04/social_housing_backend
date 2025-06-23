from rest_framework import serializers
from .models import Chambre

class ChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chambre
        fields = [
            'id', 'maison', 'titre', 'description', 'taille', 'type',
            'meublee', 'salle_de_bain', 'prix', 'disponible', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 