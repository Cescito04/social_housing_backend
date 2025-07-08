from rest_framework import serializers
from .models import Contrat
from apps.chambres.models import Chambre
from apps.utilisateurs.models import Utilisateur

class ContratSerializer(serializers.ModelSerializer):
    chambre = serializers.PrimaryKeyRelatedField(queryset=Chambre.objects.all())
    maison = serializers.SerializerMethodField()
    locataire_info = serializers.SerializerMethodField()

    def get_maison(self, obj):
        return obj.chambre.maison.id if obj.chambre and obj.chambre.maison else None

    def get_locataire_info(self, obj):
        user = obj.locataire
        return {
            'id': user.id,
            'email': user.email,
            'first_name': getattr(user, 'first_name', ''),
            'last_name': getattr(user, 'last_name', ''),
            'username': getattr(user, 'username', ''),
        } if user else None

    class Meta:
        model = Contrat
        fields = [
            'id', 'locataire', 'locataire_info', 'chambre', 'maison', 'date_debut', 'date_fin', 'montant_caution',
            'mois_caution', 'description', 'mode_paiement', 'periodicite', 'statut', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le', 'locataire'] 