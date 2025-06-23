# 🚀 Guide de Démarrage Rapide - Social Logement Backend

## Installation Express

### 1. Prérequis
- Docker et Docker Compose installés
- Git

### 2. Cloner et Configurer
```bash
git clone <repository-url>
cd social_housing_backend
cp env.example .env
```

### 3. Lancer le Projet
```bash
# Option 1: Script automatique
./start.sh

# Option 2: Makefile
make install

# Option 3: Docker Compose manuel
docker-compose up --build -d
```

### 4. Accès aux Services
- **API** : http://localhost:8000/api/
- **Swagger** : http://localhost:8000/swagger/
- **Admin** : http://localhost:8000/admin/

## 🛠️ Commandes Utiles

### Avec Makefile
```bash
make help          # Afficher toutes les commandes
make start         # Démarrer le projet
make stop          # Arrêter le projet
make restart       # Redémarrer le projet
make logs          # Voir les logs
make test          # Lancer les tests
make superuser     # Créer un superutilisateur
make shell         # Ouvrir le shell Django
```

### Avec Docker Compose
```bash
docker-compose up -d                    # Démarrer
docker-compose down                     # Arrêter
docker-compose logs -f                  # Voir les logs
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 📝 Tests Rapides

### 1. Test d'Inscription
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "telephone": "+1234567890",
    "cni": "123456789",
    "role": "proprietaire",
    "password": "testpass123",
    "password_confirmation": "testpass123"
  }'
```

### 2. Test de Connexion
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 3. Test du Profil (avec token)
```bash
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔧 Développement

### Mode Développement
```bash
# Avec volumes montés pour le hot reload
docker-compose -f docker-compose.dev.yml up --build
```

### Outils de Développement
```bash
# Installer les outils de dev
pip install -r requirements-dev.txt

# Formater le code
black .
isort .

# Linting
flake8 .

# Tests
pytest
```

### Pre-commit Hooks
```bash
pre-commit install
pre-commit run --all-files
```

## 🐛 Dépannage

### Problème de Base de Données
```bash
# Redémarrer la base de données
docker-compose restart db

# Vérifier les logs
docker-compose logs db
```

### Problème de Ports
```bash
# Vérifier les ports utilisés
lsof -i :8000
lsof -i :5432

# Arrêter et relancer
docker-compose down
docker-compose up -d
```

### Problème de Permissions
```bash
# Donner les permissions au script
chmod +x start.sh

# Nettoyer les conteneurs
docker-compose down -v
docker system prune -f
```

## 📚 Documentation Complète

Pour plus de détails, consultez le [README.md](README.md) principal.

## 🆘 Support

En cas de problème :
1. Vérifiez les logs : `docker-compose logs -f`
2. Consultez la documentation Swagger : http://localhost:8000/swagger/
3. Vérifiez la configuration dans `.env` 