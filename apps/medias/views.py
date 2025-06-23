from rest_framework import viewsets, permissions, filters
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .models import Media
from .serializers import MediaSerializer
from .permissions import IsOwnerOfChambreMedia

class MediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfChambreMedia]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['type', 'description']
    ordering_fields = ['cree_le']
    filterset_fields = ['type', 'chambre']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'proprietaire':
            return Media.objects.filter(chambre__maison__proprietaire=user)
        return Media.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        chambre = serializer.validated_data['chambre']
        if hasattr(user, 'role') and user.role == 'proprietaire':
            if chambre.maison.proprietaire != user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Vous ne pouvez ajouter des médias qu'à vos propres chambres.")
        serializer.save()

    @swagger_auto_schema(tags=['Médias'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Médias'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Médias'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Médias'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Médias'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Médias'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 