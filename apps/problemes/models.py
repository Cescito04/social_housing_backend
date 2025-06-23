from django.db import models
from django.conf import settings
from apps.contrats.models import Contrat

class Probleme(models.Model):
    TYPE_CHOICES = [
        ('plomberie', 'Plomberie'),
        ('electricite', 'Électricité'),
        ('autre', 'Autre'),
    ]
    RESPONSABLE_CHOICES = [
        ('locataire', 'Locataire'),
        ('proprietaire', 'Propriétaire'),
    ]
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='problemes')
    signale_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='problemes_signales')
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    responsable = models.CharField(max_length=20, choices=RESPONSABLE_CHOICES)
    resolu = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Problème {self.id} - {self.contrat} - {self.type}" 