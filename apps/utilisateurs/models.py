from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé pour l'application de logement social.
    """
    
    # Rôles disponibles
    ROLE_CHOICES = [
        ('proprietaire', 'Propriétaire'),
        ('locataire', 'Locataire'),
    ]
    
    # Champs personnalisés
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email",
        help_text="L'adresse email sera utilisée comme identifiant de connexion"
    )
    
    telephone = models.CharField(
        max_length=15,
        verbose_name="Numéro de téléphone",
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
            )
        ]
    )
    
    cni = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro CNI",
        help_text="Numéro de la carte nationale d'identité"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name="Rôle",
        help_text="Rôle de l'utilisateur dans le système"
    )
    
    # Configuration du modèle
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'telephone', 'cni', 'role']
    
    # Métadonnées
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        db_table = 'utilisateurs'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def is_proprietaire(self):
        """Vérifie si l'utilisateur est un propriétaire."""
        return self.role == 'proprietaire'
    
    def is_locataire(self):
        """Vérifie si l'utilisateur est un locataire."""
        return self.role == 'locataire' 