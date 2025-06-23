from rest_framework import serializers
from .models import Maison

class MaisonSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)

    class Meta:
        model = Maison
        fields = ['id', 'proprietaire', 'adresse', 'latitude', 'longitude', 'description', 'cree_le']
        read_only_fields = ['id', 'proprietaire', 'cree_le'] 