from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "app_dxr"

router = DefaultRouter()
router.register(r'locations', DxRLocationViewSet, basename='dxr-location')
router.register(r'dxr-links', DxRViewSet, basename='dxr')
router.register(r'attachments', DxRAttachmentViewSet, basename='dxr-attachment')
router.register(r'comments', DxRCommentViewSet, basename='dxr-comment')

urlpatterns = [
    path('', include(router.urls)),
]