from rest_framework import viewsets, permissions, filters, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contrat
from .serializers import ContratSerializer
from .permissions import IsOwnerOrLocataire

class ContratViewSet(viewsets.ModelViewSet):
    serializer_class = ContratSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrLocataire]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['statut', 'date_debut', 'date_fin']
    ordering_fields = ['date_debut', 'date_fin', 'cree_le']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'proprietaire':
            # Propriétaire : contrats des chambres de ses maisons
            return Contrat.objects.filter(chambre__maison__proprietaire=user)
        elif hasattr(user, 'role') and user.role == 'locataire':
            # Locataire : ses propres contrats
            return Contrat.objects.filter(locataire=user)
        return Contrat.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        chambre = serializer.validated_data['chambre']
        # Vérifie que la chambre est disponible
        if not chambre.disponible:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Cette chambre n'est plus disponible.")
        # Si propriétaire, vérifie qu'il possède la chambre
        if hasattr(user, 'role') and user.role == 'proprietaire':
            if chambre.maison.proprietaire != user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Vous ne pouvez créer un contrat que pour vos propres chambres.")
        # Si locataire, il peut louer n'importe quelle chambre disponible
        serializer.save(locataire=user)
        # Marque la chambre comme non disponible
        chambre.disponible = False
        chambre.save(update_fields=['disponible'])

    @swagger_auto_schema(tags=['Contrats'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Contrats'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Contrats'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Contrats'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Contrats'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Contrats'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='resilier', permission_classes=[permissions.IsAuthenticated, IsOwnerOrLocataire])
    @swagger_auto_schema(tags=['Contrats'], operation_summary="Résilier un contrat", operation_description="Met le statut du contrat à 'resilié'.")
    def resilier(self, request, pk=None):
        contrat = self.get_object()
        if contrat.statut != 'resilie':
            contrat.statut = 'resilie'
            contrat.save(update_fields=['statut'])
        return Response({'status': 'contrat résilié'}, status=status.HTTP_200_OK) 