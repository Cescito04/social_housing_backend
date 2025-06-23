from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            'id', 'chambre', 'url', 'type', 'description', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le'] 