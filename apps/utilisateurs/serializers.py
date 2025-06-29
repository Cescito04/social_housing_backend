from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Utilisateur
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'affichage des informations utilisateur.
    """
    
    class Meta:
        model = Utilisateur
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                 'telephone', 'cni', 'role', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']


class InscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Utilisateur
        fields = ['email', 'username', 'first_name', 'last_name', 
                 'telephone', 'cni', 'role', 'password', 'password_confirmation']
    
    def validate(self, attrs):
        """Validation personnalisée pour l'inscription."""
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(
                {"password_confirmation": "Les mots de passe ne correspondent pas."}
            )
        return attrs
    
    def create(self, validated_data):
        """Création d'un nouvel utilisateur."""
        validated_data.pop('password_confirmation')
        user = Utilisateur.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer pour l'authentification JWT.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        """Validation des identifiants de connexion."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Impossible de se connecter avec les identifiants fournis.'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Ce compte utilisateur a été désactivé.'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Les champs email et mot de passe sont requis.'
            )


class UtilisateurUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour du profil utilisateur.
    """
    
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'telephone']
    
    def update(self, instance, validated_data):
        """Mise à jour du profil utilisateur."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token 