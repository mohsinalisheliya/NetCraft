from rest_framework import serializers
from .models import *

class CircuitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitType
        fields = '__all__'

class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = '__all__'

class CircuitTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitTenant
        fields = '__all__'

class CircuitTerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitTermination
        fields = '__all__'

class CircuitAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitAttachment
        fields = '__all__'

class BandwidthModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandwidthModification
        fields = '__all__'

class CircuitShiftingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitShifting
        fields = '__all__'

