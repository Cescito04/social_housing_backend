from django.db import models
from apps.chambres.models import Chambre
import os
import uuid

def media_upload_path(instance, filename):
    """Génère le chemin d'upload pour les médias avec un nom unique"""
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex[:8]
    filename = f"media_{instance.chambre.id}_{unique_id}.{ext}"
    return os.path.join('medias', f'chambre_{instance.chambre.id}', filename)

class Media(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Vidéo'),
    ]
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='medias')
    file = models.FileField(upload_to=media_upload_path, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media {self.id} - {self.chambre} - {self.type}"

    def get_url(self):
        """Retourne l'URL du fichier (locale ou externe)"""
        if self.file:
            return self.file.url
        return self.url 