import uuid
from django.http import JsonResponse
from .models import SystemLicense # <--- IMPORT CHANGE KIYA


import threading
from django.utils.deprecation import MiddlewareMixin

# Yeh memory box banayega
_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

# Naya Middleware
class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)

#--------------------------[LICENSE MIDDLEWARE]--------------------------
class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_mac_address(self):
        mac = uuid.getnode()
        return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

    def __call__(self, request):
        # 1. Bypass system routes
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/') or request.path == '/favicon.ico':
            return self.get_response(request)

        current_mac = self.get_mac_address()
        system_license = SystemLicense.objects.first()
        
        # 2. Basic License Existence & Active Status Check
        if not system_license or not system_license.license_key or not system_license.is_active:
            return JsonResponse({
                "error": "SYSTEM LOCKED", 
                "message": "Valid License Key not found or inactive. Please update the key in the Admin Panel.", 
                "your_hardware_id": current_mac
            }, status=403)

        license_key = system_license.license_key

        # 3. Hardware Validation Logic (GEZT-MNRY... type validation will come here)
        is_valid = True 
        
        if not is_valid:
            return JsonResponse({
                "error": "LICENSE EXPIRED OR INVALID", 
                "message": "This software copy is unauthorized or expired. Contact NetCraft Support.",
                "your_hardware_id": current_mac
            }, status=403)

        # 4. 🔥 THE MASTER PLAN LOGIC (Module Restriction) 🔥
        # Agar JSONField khali hai, toh empty list [] use karega
        allowed_modules = system_license.allowed_modules if system_license.allowed_modules else []
        path = request.path

        # Dictionary to map URL path to Module Name
        module_map = {
            '/api/circuit/': 'CIRCUIT',
            '/api/dxr/': 'DXR',
            '/api/network/': 'NETWORK',
            '/api/provider/': 'PROVIDER'
            # Note: Core aur CRM ko hum hamesha free/default mante hain
        }

        # Check kar agar user us module ki API hit kar raha hai jo usne nahi khareeda
        for api_path, module_name in module_map.items():
            if path.startswith(api_path) and module_name not in allowed_modules:
                return JsonResponse({
                    "error": "MODULE LOCKED", 
                    "message": f"Aapke current plan mein '{module_name}' module include nahi hai. Kripya apna plan upgrade karein.",
                    "upgrade_link": "https://netcraft.com/upgrade",
                    "your_hardware_id": current_mac
                }, status=403)

        return self.get_response(request)