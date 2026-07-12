from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "app_core"

router = DefaultRouter()
router.register(r'pop-locations', PopLocationViewSet, basename='pop-location')
router.register(r'employees', EmployeeProfileViewSet, basename='employee')
router.register(r'logs', SystemLogViewSet, basename='system-log')
router.register(r'company-profile', CompanyProfileViewSet, basename='company-profile')
router.register(r'licenses', SystemLicenseViewSet, basename='license')
router.register(r'versions', SystemVersionViewSet, basename='version')

urlpatterns = [
    # Purane wale
    path('test/', api_test_view, name='api-test'),
    path('check-update/', check_update_api, name='api-check-update'),
    path('install-update/', install_update_api, name='api-install-update'),
    path('manual-update/', manual_update_api, name='api-manual-update'),
    path('system-info/', system_info_api, name='api-system-info'),
    # Naye ViewSet wale
    path('', include(router.urls)),
]