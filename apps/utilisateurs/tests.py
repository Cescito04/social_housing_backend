from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Utilisateur


class UtilisateurModelTest(TestCase):
    """Tests pour le modèle Utilisateur."""
    
    def setUp(self):
        """Configuration initiale pour les tests."""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'telephone': '+1234567890',
            'cni': '123456789',
            'role': 'proprietaire',
            'password': 'testpass123'
        }
    
    def test_create_utilisateur(self):
        """Test de création d'un utilisateur."""
        user = Utilisateur.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.role, self.user_data['role'])
        self.assertTrue(user.check_password(self.user_data['password']))
    
    def test_email_unique(self):
        """Test que l'email doit être unique."""
        Utilisateur.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            Utilisateur.objects.create_user(**self.user_data)
    
    def test_cni_unique(self):
        """Test que le CNI doit être unique."""
        user1_data = self.user_data.copy()
        user2_data = self.user_data.copy()
        user2_data['email'] = 'test2@example.com'
        user2_data['username'] = 'testuser2'
        
        Utilisateur.objects.create_user(**user1_data)
        with self.assertRaises(Exception):
            Utilisateur.objects.create_user(**user2_data)
    
    def test_role_choices(self):
        """Test des choix de rôle."""
        user = Utilisateur.objects.create_user(**self.user_data)
        self.assertIn(user.role, ['proprietaire', 'locataire'])
    
    def test_is_proprietaire(self):
        """Test de la méthode is_proprietaire."""
        user = Utilisateur.objects.create_user(**self.user_data)
        self.assertTrue(user.is_proprietaire())
        self.assertFalse(user.is_locataire())
    
    def test_is_locataire(self):
        """Test de la méthode is_locataire."""
        user_data = self.user_data.copy()
        user_data['role'] = 'locataire'
        user = Utilisateur.objects.create_user(**user_data)
        self.assertTrue(user.is_locataire())
        self.assertFalse(user.is_proprietaire())


class UtilisateurAPITest(APITestCase):
    """Tests pour l'API utilisateurs."""
    
    def setUp(self):
        """Configuration initiale pour les tests API."""
        self.register_url = reverse('utilisateurs:inscription')
        self.login_url = reverse('utilisateurs:login')
        self.profile_url = reverse('utilisateurs:profil')
        
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'telephone': '+1234567890',
            'cni': '123456789',
            'role': 'proprietaire',
            'password': 'testpass123',
            'password_confirmation': 'testpass123'
        }
    
    def test_register_user(self):
        """Test d'inscription d'un utilisateur via API."""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        
        # Vérifier que l'utilisateur a été créé
        user = Utilisateur.objects.get(email=self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
    
    def test_register_user_invalid_data(self):
        """Test d'inscription avec des données invalides."""
        invalid_data = self.user_data.copy()
        invalid_data['password_confirmation'] = 'wrongpassword'
        
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_user(self):
        """Test de connexion d'un utilisateur via API."""
        # Créer un utilisateur d'abord
        user = Utilisateur.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password']
        )
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_login_invalid_credentials(self):
        """Test de connexion avec des identifiants invalides."""
        login_data = {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_profile_authenticated(self):
        """Test de récupération du profil utilisateur authentifié."""
        # Créer et connecter un utilisateur
        user = Utilisateur.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password']
        )
        
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
    
    def test_get_profile_unauthenticated(self):
        """Test de récupération du profil sans authentification."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile(self):
        """Test de mise à jour du profil utilisateur."""
        # Créer et connecter un utilisateur
        user = Utilisateur.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password']
        )
        
        self.client.force_authenticate(user=user)
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'telephone': '+9876543210'
        }
        
        response = self.client.put(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que les données ont été mises à jour
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Name')
        self.assertEqual(user.telephone, '+9876543210') 