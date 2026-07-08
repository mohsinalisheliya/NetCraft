from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class BtsViewSet(viewsets.ModelViewSet):
    queryset = Bts.objects.all().order_by('-created_at')
    serializer_class = BtsSerializer
    permission_classes = [IsAuthenticated]

class L2PoiViewSet(viewsets.ModelViewSet):
    queryset = L2Poi.objects.all().order_by('-created_at')
    serializer_class = L2PoiSerializer
    permission_classes = [IsAuthenticated]