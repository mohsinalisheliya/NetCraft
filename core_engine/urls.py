"""
URL configuration for core_engine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
urlpatterns = [
    path("admin/", admin.site.urls),

    path('core/', include('apps.app_core.urls')),
    path('crm/', include('apps.app_crm.urls')),
    path('provider/', include('apps.app_provider.urls')),
    path('network/', include('apps.app_network.urls')),
    path('circuit/', include('apps.app_circuit.urls')),
    path('dxr/', include('apps.app_dxr.urls')),

    #API Endpoints
    path('api/crm/', include('apps.app_crm.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/network/', include('apps.app_network.urls')), 
    path('api/provider/', include('apps.app_provider.urls')),
    

]
