#!/bin/bash

# Script de démarrage pour Social Logement Backend

echo "🚀 Démarrage du projet Social Logement Backend..."

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env à partir de env.example..."
    cp env.example .env
    echo "✅ Fichier .env créé. Veuillez le configurer selon vos besoins."
fi

# Construire et démarrer les conteneurs
echo "🐳 Construction et démarrage des conteneurs Docker..."
docker-compose up --build -d

# Attendre que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
sleep 10

# Exécuter les migrations
echo "🗄️ Exécution des migrations de base de données..."
docker-compose exec -T web python manage.py migrate

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "✅ Projet démarré avec succès!"
echo ""
echo "🌐 Accès aux services:"
echo "   - API: http://localhost:8000/api/"
echo "   - Documentation Swagger: http://localhost:8000/swagger/"
echo "   - Admin Django: http://localhost:8000/admin/"
echo ""
echo "📋 Commandes utiles:"
echo "   - Voir les logs: docker-compose logs -f"
echo "   - Arrêter: docker-compose down"
echo "   - Créer un superutilisateur: docker-compose exec web python manage.py createsuperuser" 