from django.db import models
from django.conf import settings
from apps.chambres.models import Chambre

class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]
    locataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rendezvous_locataire')
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='rendezvous')
    date_heure = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.chambre} - {self.locataire.email}" 