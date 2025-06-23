from rest_framework import serializers
from .models import Probleme

class ProblemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probleme
        fields = [
            'id', 'contrat', 'signale_par', 'description', 'type', 'responsable', 'resolu', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 