from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from .models import Utilisateur
from .serializers import (
    UtilisateurSerializer,
    InscriptionSerializer,
    LoginSerializer,
    UtilisateurUpdateSerializer
)


class ListeUtilisateursView(generics.ListAPIView):
    """
    Vue pour récupérer la liste de tous les utilisateurs.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Récupérer tous les utilisateurs",
        operation_description="Obtenir la liste paginée de tous les utilisateurs du système",
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Numéro de page (défaut: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Nombre d'éléments par page (défaut: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Liste des utilisateurs récupérée avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Nombre total d'utilisateurs"),
                        'next': openapi.Schema(type=openapi.TYPE_STRING, description="URL de la page suivante"),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, description="URL de la page précédente"),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT),
                            description="Liste des utilisateurs"
                        )
                    }
                )
            ),
            401: "Non authentifié - Token JWT requis",
            403: "Accès refusé - Permissions insuffisantes"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class InscriptionView(generics.CreateAPIView):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Inscription utilisateur",
        operation_description="Créer un nouveau compte utilisateur avec les informations fournies",
        request_body=InscriptionSerializer,
        responses={
            201: openapi.Response(
                description="Utilisateur créé avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            400: "Données invalides - Vérifiez les champs requis et les validations"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Création d'un utilisateur avec génération automatique des tokens JWT."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': UtilisateurSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    Vue pour l'authentification JWT.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Connexion utilisateur",
        operation_description="Authentifier un utilisateur avec email et mot de passe pour obtenir un token JWT",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Connexion réussie - Tokens JWT générés",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description="Token d'accès JWT"),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Token de rafraîchissement JWT"),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description="Informations de l'utilisateur")
                    }
                )
            ),
            400: "Identifiants invalides - Email ou mot de passe incorrect"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Authentification avec retour des informations utilisateur et mise à jour du last_login."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Mettre à jour le last_login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UtilisateurSerializer(user).data
        })


class ProfilUtilisateurView(generics.RetrieveUpdateAPIView):
    """
    Vue pour récupérer et mettre à jour le profil de l'utilisateur connecté.
    """
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retourne l'utilisateur connecté."""
        return self.request.user
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon la méthode HTTP."""
        if self.request.method in ['PUT', 'PATCH']:
            return UtilisateurUpdateSerializer
        return UtilisateurSerializer
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Récupérer le profil utilisateur",
        operation_description="Obtenir les informations du profil de l'utilisateur connecté",
        responses={
            200: UtilisateurSerializer,
            401: "Non authentifié - Token JWT requis"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Mettre à jour le profil utilisateur",
        operation_description="Modifier les informations du profil de l'utilisateur connecté",
        request_body=UtilisateurUpdateSerializer,
        responses={
            200: UtilisateurSerializer,
            400: "Données invalides - Vérifiez les champs fournis",
            401: "Non authentifié - Token JWT requis"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Mettre à jour partiellement le profil",
        operation_description="Modifier partiellement les informations du profil utilisateur",
        request_body=UtilisateurUpdateSerializer,
        responses={
            200: UtilisateurSerializer,
            400: "Données invalides",
            401: "Non authentifié - Token JWT requis"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    tags=['Authentification'],
    operation_summary="Vérifier l'authentification",
    operation_description="Vérifier si l'utilisateur est connecté et retourner ses informations",
    responses={
        200: openapi.Response(
            description="Utilisateur authentifié",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        401: "Non authentifié - Token JWT requis"
    }
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def verifier_authentification(request):
    """
    Vue pour vérifier si l'utilisateur est authentifié.
    """
    return Response({
        'authenticated': True,
        'user': UtilisateurSerializer(request.user).data
    })


@swagger_auto_schema(
    method='post',
    tags=['Authentification'],
    operation_summary="Déconnexion utilisateur",
    operation_description="Invalider le token JWT de l'utilisateur connecté",
    responses={
        200: openapi.Response(
            description="Déconnexion réussie",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: "Non authentifié - Token JWT requis"
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """
    Vue pour la déconnexion de l'utilisateur.
    """
    try:
        # Ici on pourrait ajouter le token à une blacklist
        # Pour l'instant, on retourne juste un message de succès
        return Response({
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Erreur lors de la déconnexion'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 