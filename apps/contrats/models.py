from django.db import models
from django.conf import settings
from apps.chambres.models import Chambre

class Contrat(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('cash', 'Cash'),
        ('virement', 'Virement'),
        ('mobile money', 'Mobile Money'),
    ]
    PERIODICITE_CHOICES = [
        ('journalier', 'Journalier'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
    ]
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('resilie', 'Résilié'),
    ]

    locataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contrats_locataire')
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='contrats')
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_caution = models.DecimalField(max_digits=10, decimal_places=2)
    mois_caution = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    periodicite = models.CharField(max_length=20, choices=PERIODICITE_CHOICES)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrat {self.id} - {self.chambre} - {self.locataire.email}" 