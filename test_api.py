#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement de l'API Social Logement.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_health_check():
    """Test de base pour vérifier que le serveur répond."""
    try:
        response = requests.get(f"{BASE_URL}/auth-check/")
        print("✅ Serveur accessible")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible. Assurez-vous que docker-compose est lancé.")
        return False

def test_register():
    """Test d'inscription d'un utilisateur."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "telephone": "+1234567890",
        "cni": "123456789",
        "role": "proprietaire",
        "password": "testpassword123",
        "password_confirmation": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register/", json=user_data)
        if response.status_code == 201:
            print("✅ Inscription réussie")
            return response.json()
        else:
            print(f"❌ Échec de l'inscription: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Erreur lors de l'inscription: {e}")
        return None

def test_login():
    """Test de connexion."""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token/", json=login_data)
        if response.status_code == 200:
            print("✅ Connexion réussie")
            return response.json()
        else:
            print(f"❌ Échec de la connexion: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return None

def test_profile(access_token):
    """Test de récupération du profil utilisateur."""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/me/", headers=headers)
        if response.status_code == 200:
            print("✅ Récupération du profil réussie")
            return response.json()
        else:
            print(f"❌ Échec de la récupération du profil: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du profil: {e}")
        return None

def main():
    """Fonction principale de test."""
    print("🧪 Tests de l'API Social Logement")
    print("=" * 40)
    
    # Test de santé
    if not test_health_check():
        return
    
    # Test d'inscription
    register_result = test_register()
    if not register_result:
        print("⚠️ Impossible de tester l'inscription")
        return
    
    # Attendre un peu
    time.sleep(1)
    
    # Test de connexion
    login_result = test_login()
    if not login_result:
        print("⚠️ Impossible de tester la connexion")
        return
    
    # Test du profil
    access_token = login_result.get('access')
    if access_token:
        test_profile(access_token)
    
    print("\n🎉 Tous les tests sont terminés!")

if __name__ == "__main__":
    main() 