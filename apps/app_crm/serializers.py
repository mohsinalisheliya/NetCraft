from rest_framework import serializers
from .models import *

class CustomerAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAttachment
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    
    attachments = CustomerAttachmentSerializer(many=True, read_only=True)
    has_active_links = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = '__all__'