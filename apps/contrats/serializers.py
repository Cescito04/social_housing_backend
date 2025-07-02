from rest_framework import serializers
from .models import Contrat

class ContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = [
            'id', 'locataire', 'chambre', 'date_debut', 'date_fin', 'montant_caution',
            'mois_caution', 'description', 'mode_paiement', 'periodicite', 'statut', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le', 'locataire'] 