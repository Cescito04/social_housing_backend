from rest_framework.routers import DefaultRouter
from .views import ContratViewSet

router = DefaultRouter()
router.register(r'', ContratViewSet, basename='contrat')

urlpatterns = router.urls 