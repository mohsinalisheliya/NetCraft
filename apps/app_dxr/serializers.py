from rest_framework import serializers
from .models import *

class DxRLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DxRLocation
        fields = '__all__'

class DxRAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DxRAttachment
        fields = '__all__'

class DxRCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DxRComment
        fields = '__all__'

class DxRSerializer(serializers.ModelSerializer):
    attachments = DxRAttachmentSerializer(many=True, read_only=True)
    comments = DxRCommentSerializer(many=True, read_only=True)

    class Meta:
        model = DxR
        fields = '__all__'