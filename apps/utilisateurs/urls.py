from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    # Endpoints d'authentification
    path('register/', views.InscriptionView.as_view(), name='inscription'),
    path('token/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Endpoints de gestion des utilisateurs
    path('users/', views.ListeUtilisateursView.as_view(), name='liste_utilisateurs'),
    path('me/', views.ProfilUtilisateurView.as_view(), name='profil'),
    path('auth-check/', views.verifier_authentification, name='verifier_authentification'),
] 