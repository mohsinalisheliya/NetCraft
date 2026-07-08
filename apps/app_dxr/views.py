from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class DxRLocationViewSet(viewsets.ModelViewSet):
    queryset = DxRLocation.objects.all().order_by('-id')
    serializer_class = DxRLocationSerializer
    permission_classes = [IsAuthenticated]

class DxRViewSet(viewsets.ModelViewSet):
    queryset = DxR.objects.all().order_by('-created_at')
    serializer_class = DxRSerializer
    permission_classes = [IsAuthenticated]

class DxRAttachmentViewSet(viewsets.ModelViewSet):
    queryset = DxRAttachment.objects.all().order_by('-uploaded_at')
    serializer_class = DxRAttachmentSerializer
    permission_classes = [IsAuthenticated]

class DxRCommentViewSet(viewsets.ModelViewSet):
    queryset = DxRComment.objects.all().order_by('-created_at')
    serializer_class = DxRCommentSerializer
    permission_classes = [IsAuthenticated]