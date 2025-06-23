from rest_framework import viewsets, permissions, filters, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Probleme
from .serializers import ProblemeSerializer
from .permissions import IsLocataireOrProprietaireProbleme

class ProblemeViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemeSerializer
    permission_classes = [permissions.IsAuthenticated, IsLocataireOrProprietaireProbleme]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['description', 'type']
    ordering_fields = ['cree_le']
    filterset_fields = ['type', 'resolu', 'responsable']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'locataire':
            return Probleme.objects.filter(contrat__locataire=user)
        elif hasattr(user, 'role') and user.role == 'proprietaire':
            return Probleme.objects.filter(contrat__chambre__maison__proprietaire=user)
        return Probleme.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        contrat = serializer.validated_data['contrat']
        if hasattr(user, 'role') and user.role == 'locataire':
            if contrat.locataire != user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Vous ne pouvez signaler un problème que sur vos propres contrats.")
        serializer.save(signale_par=user)

    @swagger_auto_schema(tags=['Problèmes'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Problèmes'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Problèmes'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Problèmes'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Problèmes'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Problèmes'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='resoudre', permission_classes=[permissions.IsAuthenticated, IsLocataireOrProprietaireProbleme])
    @swagger_auto_schema(tags=['Problèmes'], operation_summary="Marquer un problème comme résolu", operation_description="Change le statut du problème à résolu.")
    def resoudre(self, request, pk=None):
        probleme = self.get_object()
        if not probleme.resolu:
            probleme.resolu = True
            probleme.save(update_fields=['resolu'])
        return Response({'status': 'problème résolu'}, status=status.HTTP_200_OK) 