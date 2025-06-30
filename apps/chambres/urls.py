from django.urls import path
from .views import ChambreViewSet

chambre_list = ChambreViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
chambre_detail = ChambreViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('chambres/', chambre_list, name='chambre-list'),
    path('chambres/<int:pk>/', chambre_detail, name='chambre-detail'),
] 