# 🏠 Social Housing Backend API

Backend Django moderne pour la gestion de logements sociaux avec authentification JWT, API REST complète et gestion avancée des contrats de location.

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies Utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Modèles de Données](#-modèles-de-données)
- [Authentification](#-authentification)
- [Déploiement](#-déploiement)
- [Développement](#-développement)
- [Tests](#-tests)

## ✨ Fonctionnalités

### 🔐 Authentification & Sécurité
- **Authentification JWT** avec tokens d'accès et de rafraîchissement
- **Modèle utilisateur personnalisé** avec rôles (propriétaire/locataire)
- **Validation des données** avec sérialiseurs Django REST Framework
- **Permissions granulaires** par rôle et par ressource
- **Protection CSRF** et validation des tokens

### 🏘️ Gestion des Propriétés
- **CRUD complet** pour les maisons et chambres
- **Géolocalisation** avec coordonnées GPS
- **Gestion des disponibilités** des chambres
- **Validation des données** et contraintes métier
- **Permissions basées sur la propriété** (propriétaire uniquement)

### 📋 Gestion des Contrats
- **Création automatisée** des contrats avec assignation du locataire
- **Validation des données** en temps réel
- **Gestion des cautions** et modes de paiement
- **Suivi des statuts** (actif, terminé, annulé)
- **Permissions différenciées** selon le rôle

### 💰 Gestion Financière
- **Suivi des paiements** de loyer
- **Gestion des cautions** et remboursements
- **Historique des transactions**
- **Validation des montants** et échéances

### 🔧 Gestion des Problèmes
- **Signalement** de problèmes techniques
- **Suivi des réparations** et maintenance
- **Communication** propriétaire-locataire
- **Statuts de progression** des problèmes

### 📅 Gestion des Rendez-vous
- **Planification** de visites de propriétés
- **Calendrier interactif** via API
- **Notifications** et rappels
- **Gestion des disponibilités**

### 📸 Gestion des Médias
- **Upload et stockage** de photos/vidéos
- **Association** aux chambres et propriétés
- **Validation des formats** et tailles
- **Optimisation** des images

## 🛠️ Technologies Utilisées

### Backend
- **Django 4.2** - Framework web Python robuste
- **Django REST Framework** - API REST moderne
- **PostgreSQL** - Base de données relationnelle
- **JWT** - Authentification sécurisée
- **Django CORS Headers** - Gestion CORS

### Outils de Développement
- **Docker & Docker Compose** - Conteneurisation
- **Pytest** - Tests automatisés
- **Black** - Formatage de code Python
- **Flake8** - Linting et qualité de code
- **Swagger/OpenAPI** - Documentation API

### Sécurité
- **JWT Authentication** - Tokens sécurisés
- **Django Permissions** - Contrôle d'accès granulaire
- **Validation des données** - Sécurité des entrées
- **CSRF Protection** - Protection contre les attaques

## 🚀 Installation

### Prérequis
- **Docker** et **Docker Compose**
- **Git**

### 1. Cloner le Repository
```bash
git clone https://github.com/your-username/social_housing_backend.git
cd social_housing_backend
```

### 2. Configuration de l'Environnement
```bash
cp env.example .env
```

Éditez le fichier `.env` avec vos configurations :
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Settings
DB_NAME=social_logement_db
DB_USER=social_logement_user
DB_PASSWORD=social_logement_password
DB_HOST=db
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### 3. Lancer avec Docker
```bash
# Construction et démarrage
docker-compose up --build

# En arrière-plan
docker-compose up -d --build
```

### 4. Initialisation de la Base de Données
```bash
# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Créer un superutilisateur (optionnel)
docker-compose exec web python manage.py createsuperuser
```

## 🌐 Accès aux Services

- **API REST** : http://localhost:8000/api/
- **Documentation Swagger** : http://localhost:8000/swagger/
- **Admin Django** : http://localhost:8000/admin/
- **Base de données** : localhost:5432

## 🔌 API Endpoints

### 🔐 Authentification
```http
POST /api/register/                    # Inscription utilisateur
POST /api/token/                       # Connexion JWT
POST /api/token/refresh/               # Rafraîchir le token JWT
GET  /api/auth-check/                  # Vérifier l'authentification
```

### 👤 Utilisateurs
```http
GET  /api/me/                          # Profil utilisateur connecté
PUT  /api/me/                          # Mettre à jour le profil
PATCH /api/me/                         # Mise à jour partielle
```

### 🏘️ Maisons
```http
GET    /api/maisons/                   # Liste des maisons
POST   /api/maisons/                   # Créer une maison
GET    /api/maisons/{id}/              # Détails d'une maison
PUT    /api/maisons/{id}/              # Modifier une maison
DELETE /api/maisons/{id}/              # Supprimer une maison
```

### 🛏️ Chambres
```http
GET    /api/maisons/{id}/chambres/     # Chambres d'une maison
POST   /api/maisons/{id}/chambres/     # Créer une chambre
GET    /api/chambres/{id}/             # Détails d'une chambre
PUT    /api/chambres/{id}/             # Modifier une chambre
DELETE /api/chambres/{id}/             # Supprimer une chambre
```

### 📋 Contrats
```http
GET    /api/contrats/                  # Liste des contrats
POST   /api/contrats/                  # Créer un contrat
GET    /api/contrats/{id}/             # Détails d'un contrat
DELETE /api/contrats/{id}/             # Annuler un contrat
```

### 💰 Paiements
```http
GET    /api/paiements/                 # Liste des paiements
POST   /api/paiements/                 # Créer un paiement
GET    /api/paiements/{id}/            # Détails d'un paiement
PUT    /api/paiements/{id}/            # Modifier un paiement
```

### 🔧 Problèmes
```http
GET    /api/problemes/                 # Liste des problèmes
POST   /api/problemes/                 # Signaler un problème
GET    /api/problemes/{id}/            # Détails d'un problème
PUT    /api/problemes/{id}/            # Modifier un problème
```

### 📅 Rendez-vous
```http
GET    /api/rendezvous/                # Liste des rendez-vous
POST   /api/rendezvous/                # Créer un rendez-vous
GET    /api/rendezvous/{id}/           # Détails d'un rendez-vous
PUT    /api/rendezvous/{id}/           # Modifier un rendez-vous
```

### 📸 Médias
```http
GET    /api/medias/                    # Liste des médias
POST   /api/medias/                    # Upload d'un média
GET    /api/medias/{id}/               # Détails d'un média
DELETE /api/medias/{id}/               # Supprimer un média
```

## 📊 Modèles de Données

### 👤 Utilisateur
```python
class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, validators=[phone_regex])
    cni = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
```

### 🏘️ Maison
```python
class Maison(models.Model):
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
```

### 🛏️ Chambre
```python
class Chambre(models.Model):
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    taille = models.DecimalField(max_digits=5, decimal_places=2)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
```

### 📋 Contrat
```python
class Contrat(models.Model):
    locataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_caution = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=PAIEMENT_CHOICES)
    periodicite = models.CharField(max_length=20, choices=PERIODICITE_CHOICES)
```

## 🔐 Authentification

### JWT Configuration
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Exemple d'Utilisation
```bash
# Connexion
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Utilisation du token
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🐳 Commandes Docker Utiles

```bash
# Lancer le projet
docker-compose up

# Lancer en arrière-plan
docker-compose up -d

# Arrêter le projet
docker-compose down

# Voir les logs
docker-compose logs -f

# Reconstruire les images
docker-compose up --build

# Exécuter des commandes Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Accéder au shell Django
docker-compose exec web python manage.py shell

# Lancer les tests
docker-compose exec web python -m pytest

# Redémarrer un service
docker-compose restart web
```

## 🧪 Tests

### Lancer les Tests
```bash
# Tous les tests
docker-compose exec web python -m pytest

# Tests avec couverture
docker-compose exec web python -m pytest --cov=apps

# Tests spécifiques
docker-compose exec web python -m pytest apps/utilisateurs/tests/
```

### Structure des Tests
```
apps/
├── utilisateurs/
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_serializers.py
├── maisons/
│   └── tests/
└── contrats/
    └── tests/
```

## 🔧 Développement

### Scripts Utiles
```bash
# Formatage du code
docker-compose exec web black .

# Linting
docker-compose exec web flake8

# Vérification des migrations
docker-compose exec web python manage.py makemigrations --dry-run

# Créer des migrations
docker-compose exec web python manage.py makemigrations

# Appliquer les migrations
docker-compose exec web python manage.py migrate
```

### Variables d'Environnement de Développement
```env
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 🚀 Déploiement

### Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Docker Production
```bash
# Construire pour la production
docker-compose -f docker-compose.prod.yml up --build

# Variables d'environnement de production
cp env.example .env.prod
# Éditer .env.prod avec les valeurs de production
```

## 📝 Exemples d'Utilisation

### Création d'un Contrat
```bash
curl -X POST http://localhost:8000/api/contrats/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chambre": 1,
    "date_debut": "2024-01-01",
    "date_fin": "2024-12-31",
    "montant_caution": 500.00,
    "mode_paiement": "virement",
    "periodicite": "mensuel"
  }'
```

### Mise à Jour d'un Profil
```bash
curl -X PUT http://localhost:8000/api/me/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "+1234567890"
  }'
```

## 🤝 Contribution

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité
3. **Commitez** vos changements
4. **Poussez** vers la branche
5. **Ouvrez** une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation de l'API
- Contactez l'équipe de développement 