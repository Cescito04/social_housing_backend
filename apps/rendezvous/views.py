from rest_framework import viewsets, permissions, filters, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import RendezVous
from .serializers import RendezVousSerializer
from .permissions import IsLocataireOrProprietaireRendezVous

class RendezVousViewSet(viewsets.ModelViewSet):
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated, IsLocataireOrProprietaireRendezVous]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['statut']
    ordering_fields = ['date_heure', 'cree_le']
    filterset_fields = ['statut', 'date_heure']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'locataire':
            return RendezVous.objects.filter(locataire=user)
        elif hasattr(user, 'role') and user.role == 'proprietaire':
            return RendezVous.objects.filter(chambre__maison__proprietaire=user)
        return RendezVous.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'locataire':
            serializer.save(locataire=user)
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les locataires peuvent créer un rendez-vous.")

    @swagger_auto_schema(tags=['Rendez-vous'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rendez-vous'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rendez-vous'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rendez-vous'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rendez-vous'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rendez-vous'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='changer-statut', permission_classes=[permissions.IsAuthenticated, IsLocataireOrProprietaireRendezVous])
    @swagger_auto_schema(tags=['Rendez-vous'], operation_summary="Changer le statut du rendez-vous", operation_description="Permet au propriétaire de confirmer ou annuler le rendez-vous.", request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={"statut": openapi.Schema(type=openapi.TYPE_STRING, enum=["confirme", "annule"])}))
    def changer_statut(self, request, pk=None):
        rendezvous = self.get_object()
        user = request.user
        if hasattr(user, 'role') and user.role == 'proprietaire' and rendezvous.chambre.maison.proprietaire == user:
            statut = request.data.get('statut')
            if statut in ['confirme', 'annule']:
                rendezvous.statut = statut
                rendezvous.save(update_fields=['statut'])
                return Response({'status': f'Rendez-vous {statut}'}, status=status.HTTP_200_OK)
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN) 