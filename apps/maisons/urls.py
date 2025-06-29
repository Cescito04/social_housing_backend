from rest_framework.routers import DefaultRouter
from .views import MaisonViewSet

router = DefaultRouter()
router.register(r'', MaisonViewSet, basename='maison')

urlpatterns = router.urls 