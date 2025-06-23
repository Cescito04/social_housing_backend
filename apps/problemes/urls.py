from rest_framework.routers import DefaultRouter
from .views import ProblemeViewSet

router = DefaultRouter()
router.register(r'problemes', ProblemeViewSet, basename='probleme')

urlpatterns = router.urls 