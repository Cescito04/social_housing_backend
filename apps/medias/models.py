from django.db import models
from apps.chambres.models import Chambre

class Media(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Vidéo'),
    ]
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='medias')
    url = models.URLField(max_length=500)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media {self.id} - {self.chambre} - {self.type}" 