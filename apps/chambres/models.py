from django.db import models
from apps.maisons.models import Maison

class Chambre(models.Model):
    TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('appartement', 'Appartement'),
        ('maison', 'Maison'),
    ]

    maison = models.ForeignKey(Maison, on_delete=models.CASCADE, related_name='chambres')
    titre = models.CharField(max_length=100)
    description = models.TextField()
    taille = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    meublee = models.BooleanField(default=False)
    salle_de_bain = models.BooleanField(default=False)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.maison.adresse})" 