import uuid
from django.http import JsonResponse
from .models import SystemLicense # <--- IMPORT CHANGE KIYA

class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_mac_address(self):
        mac = uuid.getnode()
        return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/') or request.path == '/favicon.ico' :
            return self.get_response(request)

        current_mac = self.get_mac_address()

        # AB NAYE MODEL SE DATA CHECK HOGA
        system_license = SystemLicense.objects.first()
        
        if not system_license or not system_license.license_key or not system_license.is_active:
            return JsonResponse({
                "error": "SYSTEM LOCKED", 
                "message": "Valid License Key not found or inactive. Please update the key in the Admin Panel.", 
                "your_hardware_id": current_mac
            }, status=403)

        license_key = system_license.license_key

        # Tera Billofy wala GEZT-MNRY... validation logic yahan aayega baad mein
        is_valid = True 
        
        if not is_valid:
            return JsonResponse({
                "error": "LICENSE EXPIRED OR INVALID", 
                "message": "This software copy is unauthorized or expired. Contact NetCraft Support.",
                "your_hardware_id": current_mac
            }, status=403)

        return self.get_response(request)