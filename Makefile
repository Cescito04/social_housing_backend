.PHONY: help install start stop restart logs test lint format clean migrate superuser shell

help: ## Afficher cette aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installer les dépendances et configurer le projet
	@echo "📦 Installation du projet..."
	cp env.example .env
	@echo "✅ Fichier .env créé. Veuillez le configurer."
	@echo "🚀 Lancement du projet..."
	docker-compose up --build -d
	@echo "⏳ Attente que les services soient prêts..."
	sleep 15
	docker-compose exec -T web python manage.py migrate
	docker-compose exec -T web python manage.py collectstatic --noinput
	@echo "✅ Installation terminée!"

start: ## Démarrer le projet
	@echo "🚀 Démarrage du projet..."
	docker-compose up -d
	@echo "✅ Projet démarré!"

stop: ## Arrêter le projet
	@echo "🛑 Arrêt du projet..."
	docker-compose down
	@echo "✅ Projet arrêté!"

restart: ## Redémarrer le projet
	@echo "🔄 Redémarrage du projet..."
	docker-compose restart
	@echo "✅ Projet redémarré!"

logs: ## Afficher les logs
	docker-compose logs -f

test: ## Lancer les tests
	@echo "🧪 Lancement des tests..."
	docker-compose exec web python manage.py test
	@echo "✅ Tests terminés!"

test-coverage: ## Lancer les tests avec couverture
	@echo "🧪 Lancement des tests avec couverture..."
	docker-compose exec web python manage.py test --verbosity=2 --keepdb
	@echo "✅ Tests avec couverture terminés!"

lint: ## Lancer le linting
	@echo "🔍 Vérification du code..."
	docker-compose exec web flake8 .
	@echo "✅ Linting terminé!"

format: ## Formater le code
	@echo "🎨 Formatage du code..."
	docker-compose exec web black .
	docker-compose exec web isort .
	@echo "✅ Formatage terminé!"

clean: ## Nettoyer les conteneurs et volumes
	@echo "🧹 Nettoyage..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Nettoyage terminé!"

migrate: ## Exécuter les migrations
	@echo "🗄️ Exécution des migrations..."
	docker-compose exec web python manage.py migrate
	@echo "✅ Migrations terminées!"

makemigrations: ## Créer les migrations
	@echo "📝 Création des migrations..."
	docker-compose exec web python manage.py makemigrations
	@echo "✅ Migrations créées!"

superuser: ## Créer un superutilisateur
	@echo "👤 Création d'un superutilisateur..."
	docker-compose exec web python manage.py createsuperuser
	@echo "✅ Superutilisateur créé!"

shell: ## Ouvrir le shell Django
	@echo "🐍 Ouverture du shell Django..."
	docker-compose exec web python manage.py shell

collectstatic: ## Collecter les fichiers statiques
	@echo "📁 Collecte des fichiers statiques..."
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "✅ Fichiers statiques collectés!"

dev: ## Mode développement avec volumes montés
	@echo "🔧 Mode développement..."
	docker-compose -f docker-compose.dev.yml up --build

build: ## Construire les images Docker
	@echo "🔨 Construction des images..."
	docker-compose build --no-cache
	@echo "✅ Images construites!" 