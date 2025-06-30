"""
URL configuration for social_logement project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Social Logement API",
        default_version='v1',
        description="API pour la gestion de logements sociaux",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@social-logement.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Vue personnalisée pour le rafraîchissement de token avec tags Swagger
class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Authentification'],
        operation_summary="Rafraîchir le token JWT",
        operation_description="Obtenir un nouveau token d'accès en utilisant le token de rafraîchissement",
        responses={
            200: openapi.Response(
                description="Token rafraîchi avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description="Nouveau token d'accès JWT")
                    }
                )
            ),
            401: "Token de rafraîchissement invalide ou expiré"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/', include('apps.utilisateurs.urls')),
    path('api/maisons/', include('apps.maisons.urls')),
    path('api/', include('apps.chambres.urls')),
    path('api/contrats/', include('apps.contrats.urls')),
    path('api/paiements/', include('apps.paiements.urls')),
    path('api/rendez-vous/', include('apps.rendezvous.urls')),
    path('api/medias/', include('apps.medias.urls')),
    path('api/problemes/', include('apps.problemes.urls')),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
            name='schema-redoc'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 