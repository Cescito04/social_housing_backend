from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Maison
from .serializers import MaisonSerializer
from .permissions import IsOwner

class MaisonViewSet(viewsets.ModelViewSet):
    serializer_class = MaisonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Maison.objects.filter(proprietaire=self.request.user)

    def perform_create(self, serializer):
        serializer.save(proprietaire=self.request.user)

    @swagger_auto_schema(tags=['Maisons'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Maisons'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Maisons'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['adresse', 'description'],
            properties={
                'adresse': openapi.Schema(type=openapi.TYPE_STRING),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', nullable=True),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', nullable=True),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Maisons'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Maisons'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Maisons'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 