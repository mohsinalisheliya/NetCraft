from rest_framework import serializers
from .models import *

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class ProviderNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderNetwork
        fields = '__all__'