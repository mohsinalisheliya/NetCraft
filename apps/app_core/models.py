import uuid
from django.db import models
from django.contrib.auth.models import User

# 1. Master Pop Locations (Branches/Cities)
class PopLocation(models.Model):
    city_name = models.CharField(max_length=255, unique=True, verbose_name="City Name")
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city_name

# 2. Secure Profile Table (Linked to Default Django User)
class EmployeeProfile(models.Model):
    # ISP Specific Departments
    DEPARTMENT_CHOICES = [
        ('NOC', 'Network Operations Center (NOC)'),
        ('FIELD', 'Field & Fiber Engineering'),
        ('SUPPORT', 'Helpdesk & Customer Support'),
        ('BILLING', 'Billing & Accounts'),
        ('SALES', 'Sales & Marketing'),
        ('MANAGEMENT', 'Management / Admin'),
    ]

    # OneToOne relation with Django's highly secure default User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Custom Fields
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='NOC')
    branch = models.ForeignKey(PopLocation, on_delete=models.SET_NULL, null=True, blank=True)
    
    # SECURITY FEATURE: Registration ke baad Approve karna padega
    is_approved = models.BooleanField(default=False, verbose_name="Admin Approved?")

    def __str__(self):
        return f"{self.user.username} - {self.get_department_display()}"


# 3. System Audit Logs
class SystemLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
    ]

    username = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_type = models.CharField(max_length=100) 
    object_id = models.CharField(max_length=100, null=True) 
    details = models.TextField()  
    request_id = models.UUIDField(default=uuid.uuid4, editable=False) 
    changes = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.username} - {self.action} - {self.model_type}"
    
# 4. ISP / Company Profile (For White-Labeling & Billing)
class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255, default="My ISP Company")
    short_code = models.CharField(max_length=20, default="ISP", help_text="ID generation prefix (e.g., DIPL, XYZ, TATA)")
    
    # Contact Info
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
    
    # Billing & Banking Details
    gst_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="GST Number")
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifsc_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="IFSC Code")
    upi_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="UPI ID")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile / Settings"
        verbose_name_plural = "Company Profile / Settings"

    def save(self, *args, **kwargs):
        # SINGLETON LOGIC: Is table mein sirf 1 hi record rahega.
        if not self.pk and CompanyProfile.objects.exists():
            return  # Naya record banne se rok dega
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

# 5. System License Model (For Software Activation)
class SystemLicense(models.Model):
    license_key = models.CharField(max_length=500, unique=True, verbose_name="System License Key")
    hardware_mac = models.CharField(max_length=100, blank=True, null=True, help_text="System Hardware ID (Auto-captured)")
    
    allowed_modules = models.JSONField(default=list, help_text="Drag & Drop me select kiye gaye modules ki list")
    # TERA NAYA BLUEPRINT YAHAN HAI
    PLAN_CHOICES = [
        ('7 Days Trial', '7 Days Trial (Free)'),
        ('1 Month', '1 Month'),
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
        ('1 Year', '1 Year'),
        ('3 Years', '3 Years'),
        ('5 Years', '5 Years'),
        ('Lifetime', 'Lifetime')
    ]
    # Default plan ko Trial rakha hai, taaki naya client add karte hi pehle trial mile
    plan_type = models.CharField(max_length=50, choices=PLAN_CHOICES, default='7 Days Trial')
    
    activation_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="License Status")
    
    class Meta:
        verbose_name = "System License & Security"
        verbose_name_plural = "System License & Security"

    def save(self, *args, **kwargs):
        if not self.pk and SystemLicense.objects.exists():
            return 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"License: {self.plan_type} - Active: {self.is_active}"
    
# 6. System Versions Models

class SystemVersion(models.Model):
    current_version = models.CharField(max_length=50, default="1.0.0", verbose_name="Current Software Version")
    
    # Update ka record rakhne ke liye
    last_update_check = models.DateTimeField(auto_now=True)
    is_update_available = models.BooleanField(default=False)
    latest_version = models.CharField(max_length=50, blank=True, null=True, verbose_name="Latest Available Version")
    release_notes = models.TextField(blank=True, null=True, help_text="Naye update mein kya features aaye hain")
    download_url = models.URLField(blank=True, null=True, help_text="Naye update ki .zip file ka link")
    install_date = models.DateTimeField(auto_now=True, verbose_name="Last Installed On")

    class Meta:
        verbose_name = "System Version & Update"
        verbose_name_plural = "System Version & Updates"

    def save(self, *args, **kwargs):
        # SINGLETON LOGIC: Is table mein sirf 1 hi record rahega.
        if not self.pk and SystemVersion.objects.exists():
            return 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Current: {self.current_version} | Update Available: {self.is_update_available}"
    
