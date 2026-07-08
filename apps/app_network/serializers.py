from rest_framework import serializers
from .models import *

class BtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bts
        fields = '__all__'

class L2PoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = L2Poi
        fields = '__all__'