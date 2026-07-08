from django.urls import path, include
from rest_framework.routers import *
from .views import *

app_name = "app_crm"

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'attachments', CustomerAttachmentViewSet, basename='customer-attachment')

urlpatterns = [
    path('', include(router.urls)),
]