from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "app_provider"

router = DefaultRouter()
router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'networks', ProviderNetworkViewSet, basename='provider-network')

urlpatterns = [
    path('', include(router.urls)),
]