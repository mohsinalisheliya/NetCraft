from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


#------------------[CircuitTypeViewSet]-------------------------------
class CircuitTypeViewSet(viewsets.ModelViewSet):
    queryset = CircuitType.objects.all().order_by('-created_at')
    serializer_class = CircuitTypeSerializer
    permission_classes = [IsAuthenticated]

#------------------[CircuitViewSet]-------------------------------
class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all().order_by('-created_at')
    serializer_class = CircuitSerializer
    permission_classes = [IsAuthenticated]

#------------------[CircuitTenantViewSet]-------------------------------
class CircuitTenantViewSet(viewsets.ModelViewSet):
    queryset = CircuitTenant.objects.all().order_by('-created_at')
    serializer_class = CircuitTenantSerializer
    permission_classes = [IsAuthenticated]

#------------------[CircuitTerminationViewSet]-------------------------------
class CircuitTerminationViewSet(viewsets.ModelViewSet):
    queryset = CircuitTermination.objects.all().order_by('-created_at')
    serializer_class = CircuitTerminationSerializer
    permission_classes = [IsAuthenticated]

#------------------[CircuitAttachmentViewSet]-------------------------------
class CircuitAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CircuitAttachment.objects.all().order_by('-uploaded_at')
    serializer_class = CircuitAttachmentSerializer
    permission_classes = [IsAuthenticated]

#------------------[BandwidthModificationViewSet]-------------------------------
class BandwidthModificationViewSet(viewsets.ModelViewSet):
    queryset = BandwidthModification.objects.all().order_by('-created_at')
    serializer_class = BandwidthModificationSerializer
    permission_classes = [IsAuthenticated]

#------------------[CircuitShiftingViewSet]-------------------------------
class CircuitShiftingViewSet(viewsets.ModelViewSet):
    queryset = CircuitShifting.objects.all().order_by('-created_at')
    serializer_class = CircuitShiftingSerializer
    permission_classes = [IsAuthenticated]

#-----------------[CircuitViewSet]-------------------------------
class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all().order_by('-created_at')
    serializer_class = CircuitSerializer
    permission_classes = [IsAuthenticated]
    
    # ------------------ THE MAGIC FILTERS ------------------
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # 1. Exact Match Filters (Dropdowns ke liye)
    filterset_fields = ['customer_type', 'is_closed', 'tp_media', 'bandwidth_unit'] 
    
    # 2. Universal Search Box (Text type karne ke liye)
    search_fields = ['circuit_id', 'customer_wan_ip', 'tp_location', 'tp_company_name'] 
    
    # 3. Column Sorting (A to Z, ya New to Old)
    ordering_fields = ['created_at', 'bandwidth_value', 'po_date']