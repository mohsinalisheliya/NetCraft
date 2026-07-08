from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "app_network"

router = DefaultRouter()
router.register(r'bts', BtsViewSet, basename='bts')
router.register(r'l2poi', L2PoiViewSet, basename='l2poi')

urlpatterns = [
    path('', include(router.urls)),
]