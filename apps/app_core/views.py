
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.app_core.serializers import *
from .models import *



# VIEWS STARTING HERE

#-------------------------- API TEST VIEW -----------------------------------
@api_view(['GET'])
def api_test_view(request):
    return Response({
        "status": "Success",
        "message": "Bhai ki API makhan ki tarah chal rahi hai! Drag and Drop system loading...",
        "project": "NetCraft SaaS"
    })


#-------------------------- System Virsion VIEW -----------------------------------
@api_view(['GET'])
def check_update_api(request):
    # 1. Apna local current version nikal
    system_version = SystemVersion.objects.first()
    if not system_version:
        # Agar table khali hai toh ek default record bana de
        system_version = SystemVersion.objects.create(current_version="1.0.0")

    # 2. Master Server se data maang (Abhi hum ek fake data assume kar rahe hain)
    # Asli life mein tu yahan `response = requests.get("TERA_GITHUB_RAW_JSON_LINK").json()` likhega
    
    try:
        # SIMULATED RESPONSE (Maan le tere cloud server ne yeh bheja):
        master_data = {
            "latest_version": "1.1.0",
            "release_notes": "Bhai naya CRM Dashboard aur mast features add kiye hain!",
            "download_url": "https://example.com/downloads/netcraft_v1.1.0.zip"
        }
        
        latest_v = master_data["latest_version"]
        
        # 3. Compare kar: Kya cloud wala version local se bada hai?
        if latest_v > system_version.current_version:
            # Agar bada hai toh database mein update save kar le
            system_version.is_update_available = True
            system_version.latest_version = latest_v
            system_version.release_notes = master_data["release_notes"]
            system_version.download_url = master_data["download_url"]
            system_version.save()
            
            return Response({
                "status": "Update Available",
                "message": f"Version {latest_v} is ready to download!",
                "data": master_data
            })
        else:
            system_version.is_update_available = False
            system_version.save()
            return Response({
                "status": "Up to Date",
                "message": "You are already using the latest version."
            })

    except Exception as e:
        return Response({"error": "Failed to connect to Master Server", "details": str(e)}, status=500)
    
#-------------------------- ViewSets for Core Models -----------------------------------
class PopLocationViewSet(viewsets.ModelViewSet):
    queryset = PopLocation.objects.all().order_by('-created_at')
    serializer_class = PopLocationSerializer
    permission_classes = [IsAuthenticated]

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all().order_by('-id')
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

class SystemLogViewSet(viewsets.ModelViewSet):
    queryset = SystemLog.objects.all().order_by('-timestamp')
    serializer_class = SystemLogSerializer
    permission_classes = [IsAuthenticated]

class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all().order_by('-created_at')
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated]

class SystemLicenseViewSet(viewsets.ModelViewSet):
    queryset = SystemLicense.objects.all().order_by('-activation_date')
    serializer_class = SystemLicenseSerializer
    permission_classes = [IsAuthenticated]

class SystemVersionViewSet(viewsets.ModelViewSet):
    queryset = SystemVersion.objects.all().order_by('-last_update_check')
    serializer_class = SystemVersionSerializer
    permission_classes = [IsAuthenticated]