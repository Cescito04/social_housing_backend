from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Media
        fields = [
            'id', 'chambre', 'file', 'url', 'type', 'description', 'cree_le'
        ]
        read_only_fields = ['id', 'cree_le', 'url']

    def get_url(self, obj):
        """Retourne l'URL du fichier"""
        return obj.get_url()

    def create(self, validated_data):
        """Override create pour gérer l'upload de fichier"""
        file = self.context['request'].FILES.get('file')
        if file:
            validated_data['file'] = file
            # Déterminer le type basé sur l'extension
            file_extension = file.name.split('.')[-1].lower()
            if file_extension in ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm']:
                validated_data['type'] = 'video'
            else:
                validated_data['type'] = 'photo'
        
        return super().create(validated_data) 