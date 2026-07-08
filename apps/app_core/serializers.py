from rest_framework import serializers
from .models import *

class PopLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopLocation
        fields = '__all__'

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'

class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'

class SystemLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLicense
        fields = '__all__'

class SystemVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemVersion
        fields = '__all__'