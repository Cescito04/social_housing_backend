from django.db import models
from django.conf import settings

class Maison(models.Model):
    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='maisons'
    )
    adresse = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField()
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adresse} ({self.proprietaire.email})" 