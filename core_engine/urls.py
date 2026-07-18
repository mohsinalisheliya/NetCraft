from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 Authentication APIs (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔗 NetCraft System APIs
    path('api/core/', include('apps.app_core.urls')),
    path('api/crm/', include('apps.app_crm.urls')),
    path('api/provider/', include('apps.app_provider.urls')),
    path('api/network/', include('apps.app_network.urls')),
    path('api/circuit/', include('apps.app_circuit.urls')),
    path('api/dxr/', include('apps.app_dxr.urls')),
]