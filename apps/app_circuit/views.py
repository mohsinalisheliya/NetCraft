from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class CircuitTypeViewSet(viewsets.ModelViewSet):
    queryset = CircuitType.objects.all().order_by('-created_at')
    serializer_class = CircuitTypeSerializer
    permission_classes = [IsAuthenticated]

class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all().order_by('-created_at')
    serializer_class = CircuitSerializer
    permission_classes = [IsAuthenticated]

class CircuitTenantViewSet(viewsets.ModelViewSet):
    queryset = CircuitTenant.objects.all().order_by('-created_at')
    serializer_class = CircuitTenantSerializer
    permission_classes = [IsAuthenticated]

class CircuitTerminationViewSet(viewsets.ModelViewSet):
    queryset = CircuitTermination.objects.all().order_by('-created_at')
    serializer_class = CircuitTerminationSerializer
    permission_classes = [IsAuthenticated]

class CircuitAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CircuitAttachment.objects.all().order_by('-uploaded_at')
    serializer_class = CircuitAttachmentSerializer
    permission_classes = [IsAuthenticated]

class BandwidthModificationViewSet(viewsets.ModelViewSet):
    queryset = BandwidthModification.objects.all().order_by('-created_at')
    serializer_class = BandwidthModificationSerializer
    permission_classes = [IsAuthenticated]

class CircuitShiftingViewSet(viewsets.ModelViewSet):
    queryset = CircuitShifting.objects.all().order_by('-created_at')
    serializer_class = CircuitShiftingSerializer
    permission_classes = [IsAuthenticated]