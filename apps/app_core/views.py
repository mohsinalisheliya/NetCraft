import os
import zipfile
import requests
from io import BytesIO
from django.conf import settings
from django.core.management import *
from rest_framework.decorators import *


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

import sys
import importlib.util
from django.utils import timezone

#--------------------------[Software Name & Version]-----------------------------------
from rest_framework.permissions import AllowAny
from rest_framework import status

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
try:
    from version import SOFTWARE_NAME, SOFTWARE_VERSION
except ImportError:
    SOFTWARE_NAME = "NetCraft"
    SOFTWARE_VERSION = "1.0.0"

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_activation_key(request):
    """
    Yeh API frontend se 64-bit key legi aur verify karegi.
    """
    secret_key = request.data.get('secret_key', '')

    # 1. Strict 64-character Validation
    if not secret_key or len(secret_key) != 64:
        return Response(
            {
                "status": "error", 
                "message": f"INVALID INTEGRITY: {SOFTWARE_NAME} requires exactly 64 characters."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Note: Yahan future mein hum tere SystemLicense model se database check lagayenge.
    # Abhi ke liye agar 64 char hain, toh API pass ho jayegi.

    # 2. Success Response (Sending dynamic name back to frontend)
    return Response(
        {
            "status": "success",
            "software_name": SOFTWARE_NAME,
            "version": SOFTWARE_VERSION,
            "message": f"{SOFTWARE_NAME} Engine Initialized Successfully."
        }, 
        status=status.HTTP_200_OK
    )

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

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    
    # 🛡️ SECURITY BYPASS LOGIC:
    def get_permissions(self):
        if self.action == 'create':
            # Naya setup karte waqt (POST) kisi token ki zaroorat nahi
            return [AllowAny()]
        # Baaki sab cheezon (GET, PUT, PATCH) ke liye JWT Token compulsory hai
        return [IsAuthenticated()]
    
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

    # Security check: Sirf .zip file allow karni hai
    if not update_file.name.endswith('.zip'):
        return Response({"error": "Sirf .zip extension wali file allowed hai."}, status=400)

    try:
        project_root = settings.BASE_DIR 
        
        # 2. Extract & Overwrite Files
        print("Applying offline patch and replacing files...")
        with zipfile.ZipFile(update_file) as z:
            z.extractall(project_root) 

        # 3. Run Database Migrations
        print("Running database sync...")
        call_command('migrate')

        # ---------------------------------------------------------
        # 4. 🔥 TERA VERSION.PY WALA JAADU YAHAN CHALEGA 🔥
        # ---------------------------------------------------------
        version_file_path = os.path.join(project_root, 'version.py')
        
        if os.path.exists(version_file_path):
            # Pythonic way to load the file without restarting the server
            spec = importlib.util.spec_from_file_location("version", version_file_path)
            version_module = importlib.util.module_from_spec(spec)
            sys.modules["version"] = version_module
            spec.loader.exec_module(version_module)

            # Naye version ki details file se utha lo
            target_version = getattr(version_module, 'APP_VERSION', 'Unknown')
            features_list = getattr(version_module, 'APP_VERSION_FEATURES', [])
            new_features = "\n".join(features_list) # Array ko text bana diya
        else:
            # Agar kisi wajah se version.py nahi milti (Fall back)
            target_version = "Unknown Update"
            new_features = "No release notes found in update file."

        # 5. Update the Database Version Tracker
        system_version = SystemVersion.objects.first()
        if system_version:
            old_version = system_version.current_version
            system_version.current_version = target_version
            system_version.release_notes = new_features
            system_version.is_update_available = False # Update apply ho gaya
            system_version.latest_version = None
            system_version.save()
        else:
            old_version = "None"
            SystemVersion.objects.create(
                current_version=target_version,
                release_notes=new_features
            )

        return Response({
            "status": "Success",
            "message": f"NetCraft successfully patched from {old_version} to {target_version}!",
            "new_features": new_features,
            "rollback_info": "Agar aapne purana version upload kiya hai, toh system downgrade ho chuka hai.",
            "note": "Kripya system/server ko ek baar restart zaroor karein naye features dekhne ke liye."
        })

    except Exception as e:
        return Response({"error": "Patch apply karne mein fail ho gaya.", "details": str(e)}, status=500)

# -------------------- ABOUT SYSTEM (MASTER INFO API) --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_info_api(request):
    try:
        # 1. License Data Fetch Kar
        license_data = SystemLicense.objects.first()
        
        # 2. Database Version Data Fetch Kar
        version_data = SystemVersion.objects.first()
        
        # 3. version.py se "Release Date" Live read kar
        release_date = "Unknown"
        version_file_path = os.path.join(settings.BASE_DIR, 'version.py')
        if os.path.exists(version_file_path):
            spec = importlib.util.spec_from_file_location("version", version_file_path)
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)
            release_date = getattr(version_module, 'APP_RELEASE_DATE', 'Unknown')

        # 4. 🔥 THE EXPIRY CALCULATOR LOGIC 🔥
        remaining_days = 0
        show_expiry_warning = False
        expiry_date_str = "Lifetime"

        if license_data and license_data.expiry_date:
            today = timezone.now().date()
            delta = license_data.expiry_date - today
            remaining_days = delta.days if delta.days > 0 else 0
            expiry_date_str = license_data.expiry_date.strftime("%d %B %Y")
            
            # Agar 30 ya usse kam din bache hain (par 0 se zyada), toh warning on kar do
            if 0 < remaining_days <= 30:
                show_expiry_warning = True

        # 5. Data Format for React Frontend
        response_data = {
            "license_info": {
                "hardware_mac": license_data.hardware_mac if license_data else "Not Registered",
                "secret_key": f"********{license_data.license_key[-4:]}" if license_data and license_data.license_key else "Missing",
                "status": "Active" if license_data and license_data.is_active else "Inactive",
                "allowed_modules": license_data.allowed_modules if license_data else [],
                "expiry_date": expiry_date_str,
                "remaining_days": remaining_days,
                "show_expiry_warning": show_expiry_warning
            },
            "version_info": {
                "current_version": version_data.current_version if version_data else "v1.0.0",
                "release_date": release_date,
                "install_date": version_data.install_date.strftime("%d %B %Y, %I:%M %p") if version_data and version_data.install_date else "Unknown",
                "release_notes": version_data.release_notes if version_data else ""
            }
        }

        return Response(response_data)

    except Exception as e:
        return Response({"error": "Failed to load system info", "details": str(e)}, status=500)
    

#--------------------------[System Info API View]-----------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from version import SOFTWARE_NAME, SOFTWARE_VERSION

from django.views import View
from django.http import JsonResponse


# Ab yeh DRF (APIView) nahi, balki pure native Django View par chalega
class SystemInfoView(View):
    def get(self, request, *args, **kwargs):
        # Seedha JSON bhej do, bina kisi DRF token check ke
        return JsonResponse({
            "app_name": SOFTWARE_NAME,
            "version": SOFTWARE_VERSION
        })