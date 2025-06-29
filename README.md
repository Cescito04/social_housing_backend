# Social Logement Backend

Backend Django pour la gestion de logements sociaux avec authentification JWT et API REST.

## 🚀 Fonctionnalités

- **Framework** : Django 4.2 + Django REST Framework
- **Authentification** : JWT (JSON Web Tokens)
- **Base de données** : PostgreSQL
- **Documentation API** : Swagger/OpenAPI
- **Conteneurisation** : Docker + Docker Compose
- **Modèle utilisateur personnalisé** avec rôles (propriétaire/locataire)
- **Gestion complète des logements, chambres, contrats, paiements, problèmes, médias et rendez-vous**

## 🧩 Modules principaux

- **utilisateurs** : Gestion des utilisateurs, rôles (propriétaire/locataire), inscription, authentification, profils personnalisés.
- **maisons** : Gestion des maisons (adresse, géolocalisation, propriétaire, description).
- **chambres** : Gestion des chambres (type, taille, prix, disponibilité, équipements, lien avec maison).
- **contrats** : Gestion des contrats de location (locataire, chambre, dates, caution, mode de paiement, statut).
- **paiements** : Suivi des paiements de loyers (contrat, montant, statut, échéance, date de paiement).
- **problemes** : Signalement et suivi des problèmes (type, description, responsable, statut, contrat lié).
- **medias** : Gestion des médias associés aux chambres (photos, vidéos, description).
- **rendezvous** : Prise de rendez-vous pour visites de chambres (locataire, chambre, date/heure, statut).

## 📋 Prérequis

- Docker
- Docker Compose

## 🛠️ Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd social_housing_backend
   ```

2. **Configurer les variables d'environnement**
   ```bash
   cp env.example .env
   # Éditer le fichier .env avec vos valeurs
   ```

3. **Lancer le projet**
   ```bash
   docker-compose up --build
   ```

4. **Créer un superutilisateur (optionnel)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 🌐 Accès aux services

- **API** : http://localhost:8000/api/
- **Documentation Swagger** : http://localhost:8000/swagger/
- **Admin Django** : http://localhost:8000/admin/
- **Base de données** : localhost:5432

## 📚 Endpoints API

### Authentification
- `POST /api/register/` - Inscription utilisateur
- `POST /api/token/` - Connexion JWT
- `POST /api/token/refresh/` - Rafraîchir le token JWT

### Profil utilisateur
- `GET /api/me/` - Récupérer le profil utilisateur connecté
- `PUT /api/me/` - Mettre à jour le profil utilisateur
- `PATCH /api/me/` - Mettre à jour partiellement le profil
- `GET /api/auth-check/` - Vérifier l'authentification

## 👤 Modèle Utilisateur

Le modèle `Utilisateur` hérite d'`AbstractUser` et inclut :

- **Champs obligatoires** :
  - `email` (unique, utilisé comme USERNAME_FIELD)
  - `username`
  - `first_name`
  - `last_name`
  - `telephone` (avec validation regex)
  - `cni` (numéro CNI unique)
  - `role` (choices: propriétaire/locataire)

## 🔧 Configuration

### Variables d'environnement (.env)

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

## 🐳 Commandes Docker utiles

```bash
# Lancer le projet
docker-compose up

# Lancer en arrière-plan
docker-compose up -d

# Arrêter le projet
docker-compose down

# Voir les logs
docker-compose logs -f

# Exécuter des commandes Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Accéder au shell Django
docker-compose exec web python manage.py shell

# Redémarrer un service
docker-compose restart web
```

## 📝 Exemples d'utilisation

### Inscription d'un utilisateur

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "+1234567890",
    "cni": "123456789",
    "role": "proprietaire",
    "password": "securepassword123",
    "password_confirmation": "securepassword123"
  }'
```

### Connexion

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Accéder au profil (avec token)

```bash
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🏗️ Structure du projet

```
social_housing_backend/
├── apps/
│   ├── chambres/
│   ├── contrats/
│   ├── maisons/
│   ├── medias/
│   ├── paiements/
│   ├── problemes/
│   ├── rendezvous/
│   └── utilisateurs/
├── social_logement/
│   ├── __init__.py
│   ├── asgi.py
│   ├── management/
│   │   └── commands/
│   │       └── wait_for_db.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── env.example
├── manage.py
├── README.md
├── requirements.txt
└── ...
```

## 🔒 Sécurité

- Authentification JWT avec rotation des tokens
- Validation des mots de passe Django
- Validation des numéros de téléphone
- Protection CSRF
- Configuration CORS

## 🧪 Tests

```bash
# Lancer les tests
docker-compose exec web python manage.py test

# Lancer les tests avec couverture
docker-compose exec web python manage.py test --verbosity=2
```

## 📦 Déploiement

Le projet est configuré pour être déployé avec Docker. Pour la production :

1. Modifier `DEBUG=False` dans `.env`
2. Générer une nouvelle `SECRET_KEY`
3. Configurer les variables d'environnement de production
4. Utiliser un serveur web comme Nginx en production

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 