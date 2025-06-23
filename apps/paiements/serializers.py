from rest_framework import serializers
from .models import Paiement

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = [
            'id', 'contrat', 'montant', 'statut', 'date_echeance', 'date_paiement', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 