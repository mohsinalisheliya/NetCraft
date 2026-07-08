from django.db import models

class DxRLocation(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    def __str__(self): return f"{self.name} ({self.code})" if self.code else self.name

class DxR(models.Model):
    DXR_TYPES = (('Dark Fiber', 'Dark Fiber'), ('X-Connect', 'X-Connect'), ('Rack Space', 'Rack Space'))

    dxr_id = models.CharField(max_length=50, unique=True, blank=True)
    dxr_type = models.CharField(max_length=50, choices=DXR_TYPES)
    
    location = models.ForeignKey(DxRLocation, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- CROSS-APP LINKS ---
    provider = models.ForeignKey('app_provider.Provider', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('app_crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='dxr_customers')
    a_end_customer = models.ForeignKey('app_crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='xconnect_a_ends')
    b_end_customer = models.ForeignKey('app_crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='xconnect_b_ends')
    
    provider_circuit_id = models.CharField(max_length=100, blank=True, null=True)
    activation_on_hold = models.BooleanField(default=False, verbose_name="Activation On Hold")
    activation_hold_reason = models.TextField(blank=True, null=True)
    po_date = models.DateField(null=True, blank=True)
    install_date = models.DateField(null=True, blank=True)
    billing_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(null=True, blank=True)
    deactivation_extension_days = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    sub_customer = models.CharField(max_length=255, blank=True, null=True)

    # Dark Fiber Specific
    fiber_section_name = models.CharField(max_length=255, blank=True, null=True)
    fiber_start_location = models.CharField(max_length=255, blank=True, null=True)
    fiber_start_latlong = models.CharField(max_length=255, blank=True, null=True)
    fiber_end_location = models.CharField(max_length=255, blank=True, null=True)
    fiber_end_latlong = models.CharField(max_length=255, blank=True, null=True)
    fiber_tapping_location = models.CharField(max_length=255, blank=True, null=True)
    fiber_tapping_latlong = models.CharField(max_length=255, blank=True, null=True)
    fiber_core = models.CharField(max_length=100, blank=True, null=True)
    total_fiber_length = models.FloatField(blank=True, null=True)
    fiber_length_unit = models.CharField(max_length=10, blank=True, null=True)

    # X-Connect Specific
    ccr_id = models.CharField(max_length=100, blank=True, null=True)
    xconnect_fiber_type = models.CharField(max_length=100, blank=True, null=True)
    xconnect_port_type = models.CharField(max_length=100, default="fiber LC-LC Dual", blank=True)
    a_end_floor_address = models.CharField(max_length=255, blank=True, null=True)
    a_end_mux_details = models.CharField(max_length=255, blank=True, null=True)
    a_end_isp_mmr = models.CharField(max_length=255, blank=True, null=True)
    b_end_floor_address = models.CharField(max_length=255, blank=True, null=True)
    b_end_mux_details = models.CharField(max_length=255, blank=True, null=True)
    b_end_isp_mmr = models.CharField(max_length=255, blank=True, null=True)

    # Rack Spaces Specific
    rack_floor_address = models.CharField(max_length=255, blank=True, null=True)
    rack_space = models.CharField(max_length=100, blank=True, null=True)
    rack_from_space = models.CharField(max_length=100, blank=True, null=True)
    power_kva = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.dxr_id:
            # --- DYNAMIC COMPANY PREFIX FETCHING ---
            from apps.app_core.models import CompanyProfile
            company = CompanyProfile.objects.first()
            prefix = company.short_code if company and company.short_code else "ISP"
            # ---------------------------------------
            
            last_dxr = DxR.objects.order_by('id').last()
            new_id = last_dxr.id + 1 if last_dxr else 1
            
            # AB DIPL KI JAGAH PREFIX USE HOGA!
            self.dxr_id = f"{prefix}/DxR/{new_id}"
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.dxr_id} - {self.dxr_type}"

class DxRAttachment(models.Model):
    dxr = models.ForeignKey(DxR, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='DxR files/' , blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DxRComment(models.Model):
    dxr = models.ForeignKey(DxR, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)