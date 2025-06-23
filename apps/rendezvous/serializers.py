from rest_framework import serializers
from .models import RendezVous

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = [
            'id', 'locataire', 'chambre', 'date_heure', 'statut', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 