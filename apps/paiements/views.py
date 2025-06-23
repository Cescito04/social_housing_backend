from rest_framework import viewsets, permissions, filters
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .models import Paiement
from .serializers import PaiementSerializer
from .permissions import IsOwnerOrLocatairePaiement

class PaiementViewSet(viewsets.ModelViewSet):
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrLocatairePaiement]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['statut']
    ordering_fields = ['date_echeance', 'date_paiement', 'cree_le']
    filterset_fields = ['statut', 'contrat', 'date_echeance']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'proprietaire':
            # Propriétaire : paiements de ses contrats
            return Paiement.objects.filter(contrat__chambre__maison__proprietaire=user)
        elif hasattr(user, 'role') and user.role == 'locataire':
            # Locataire : ses propres paiements
            return Paiement.objects.filter(contrat__locataire=user)
        return Paiement.objects.none()

    @swagger_auto_schema(tags=['Paiements'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Paiements'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Paiements'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Paiements'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Paiements'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Paiements'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 