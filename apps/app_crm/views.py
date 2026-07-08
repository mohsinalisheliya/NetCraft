
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

#--------------------------- Customer ViewSet -----------------------------------
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 

#---------------------- Customer Attachment ViewSet -----------------------------
class CustomerAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CustomerAttachment.objects.all().order_by('-uploaded_at')
    serializer_class = CustomerAttachmentSerializer
    permission_classes = [IsAuthenticated] 