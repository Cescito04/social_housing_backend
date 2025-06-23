from django.db import models
from apps.contrats.models import Contrat

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('paye', 'Payé'),
        ('impaye', 'Impayé'),
    ]
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='impaye')
    date_echeance = models.DateField()
    date_paiement = models.DateTimeField(blank=True, null=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} - Contrat {self.contrat.id} - {self.montant} {self.statut}" 