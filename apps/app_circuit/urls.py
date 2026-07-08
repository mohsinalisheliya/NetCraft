from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "app_circuit"

router = DefaultRouter()
router.register(r'types', CircuitTypeViewSet, basename='circuit-type')
router.register(r'circuits', CircuitViewSet, basename='circuit')
router.register(r'tenants', CircuitTenantViewSet, basename='circuit-tenant')
router.register(r'terminations', CircuitTerminationViewSet, basename='circuit-termination')
router.register(r'attachments', CircuitAttachmentViewSet, basename='circuit-attachment')
router.register(r'modifications', BandwidthModificationViewSet, basename='bandwidth-modification')
router.register(r'shiftings', CircuitShiftingViewSet, basename='circuit-shifting')

urlpatterns = [
    path('', include(router.urls)),
]