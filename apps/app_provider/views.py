from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all().order_by('-created_at')
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]

class ProviderNetworkViewSet(viewsets.ModelViewSet):
    queryset = ProviderNetwork.objects.all().order_by('-created_at')
    serializer_class = ProviderNetworkSerializer
    permission_classes = [IsAuthenticated]