import os
import zipfile
import requests
from io import BytesIO
from django.conf import settings
from django.core.management import *
from rest_framework.decorators import *

import os
import zipfile
from django.conf import settings
from django.core.management import call_command
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import SystemVersion

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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

# -------------------- THE OTA PATCHER --------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Tijori ka lock zaroori hai!
def install_update_api(request):
    system_version = SystemVersion.objects.first()
    
    # 1. Check kar ki kya sach mein koi update available hai
    if not system_version or not system_version.is_update_available:
        return Response({"error": "Koi naya update available nahi hai."}, status=400)

    download_url = system_version.download_url
    if not download_url:
        return Response({"error": "Update file ka link nahi mila."}, status=400)

    try:
        # 2. File Download Kar
        print(f"Downloading update from: {download_url}...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status() # Agar link kharab hoga toh error phek dega

        # 3. Extract & Replace (Project Root Directory mein)
        project_root = settings.BASE_DIR # Yeh tere NetCraft folder ka main path hai
        print(f"Extracting files to {project_root}...")
        
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(project_root) # Puraane files overwrite ho jayenge

        # 4. Auto-Migrate (Database Update)
        print("Running database migrations...")
        call_command('migrate') # Yeh command background mein migrations chala degi!

        # 5. Tracker Update (Version Upgrade Kar De)
        old_version = system_version.current_version
        new_version = system_version.latest_version
        
        system_version.current_version = new_version
        system_version.is_update_available = False
        system_version.latest_version = None
        system_version.release_notes = None
        system_version.download_url = None
        system_version.save()

        return Response({
            "status": "Success",
            "message": f"NetCraft successfully updated from {old_version} to {new_version}!",
            "note": "Kripya apne server ko ek baar restart karein naye changes dekhne ke liye."
        })

    except Exception as e:
        return Response({"error": "Update install karne mein fail ho gaya.", "details": str(e)}, status=500)
    
# -------------------- OFFLINE MANUAL PATCHER (UPDATE / ROLLBACK) --------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manual_update_api(request):
    # 1. Check kar ki user ne file bheji hai ya nahi
    if 'update_file' not in request.FILES:
        return Response({"error": "Kripya .zip file upload karein."}, status=400)

    update_file = request.FILES['update_file']
    
    # User batayega ki wo kaunsa version upload kar raha hai (e.g., "1.1.1" for rollback or "1.1.2" for update)
    target_version = request.data.get('version_number', 'Unknown Version')

    # Security check: Sirf .zip file allow karni hai
    if not update_file.name.endswith('.zip'):
        return Response({"error": "Sirf .zip extension wali file allowed hai."}, status=400)

    try:
        project_root = settings.BASE_DIR 
        
        # 2. Extract & Overwrite Files directly from uploaded memory
        print(f"Applying offline patch for version {target_version}...")
        with zipfile.ZipFile(update_file) as z:
            z.extractall(project_root) # Nayi files purani files ko replace kar dengi

        # 3. Run Database Migrations (Agar naye update mein DB changes hain)
        # (Rollback ke time par migrations safe rehte hain, errors nahi aate)
        print("Running database sync...")
        call_command('migrate')

        # 4. Update the Database Version Tracker
        system_version = SystemVersion.objects.first()
        if system_version:
            old_version = system_version.current_version
            system_version.current_version = target_version
            system_version.is_update_available = False # Update apply ho gaya
            system_version.latest_version = None
            system_version.save()
        else:
            old_version = "None"
            SystemVersion.objects.create(current_version=target_version)

        return Response({
            "status": "Success",
            "message": f"NetCraft successfully patched from {old_version} to {target_version}!",
            "rollback_info": "Agar aapne purana version upload kiya hai, toh system successfully downgrade ho chuka hai.",
            "note": "Kripya system/server ko ek baar restart zaroor karein."
        })

    except Exception as e:
        return Response({"error": "Patch apply karne mein fail ho gaya.", "details": str(e)}, status=500)