from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import Chambre
from .serializers import ChambreSerializer
from .permissions import IsOwnerOfMaison

class ChambreViewSet(viewsets.ModelViewSet):
    serializer_class = ChambreSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfMaison]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Chambre.objects.none()
        return Chambre.objects.filter(maison__proprietaire=self.request.user)

    def perform_create(self, serializer):
        maison = serializer.validated_data['maison']
        if maison.proprietaire != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous ne pouvez ajouter une chambre que dans vos propres maisons.")
        serializer.save()

    @swagger_auto_schema(tags=['Chambres'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Chambres'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Chambres'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Chambres'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Chambres'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Chambres'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 