import datetime
import uuid
import pytz
from django.db import models
from django.utils import timezone

class CircuitType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Circuit Type Name")
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Circuit(models.Model):
    CUSTOMER_TYPE_CHOICES = [('B2B', 'B2B'), ('B2C', 'B2C'), ('CORE BW', 'CORE BW')]
    BANDWIDTH_UNIT_CHOICES = [('Kbps', 'Kbps'), ('Mbps', 'Mbps'), ('Gbps', 'Gbps')]
    TP_MEDIA_CHOICES = [('Wireless', 'Wireless'), ('Fiber', 'Fiber')]
    TP_BILLING_CYCLE_CHOICES = [
        ('Monthly', 'Monthly'), ('Monthly Advance', 'Monthly Advance'),
        ('Quarterly', 'Quarterly'), ('Quarterly Advance', 'Quarterly Advance'),
        ('Six Month', 'Six Month'), ('Six Month Advance', 'Six Month Advance'),
        ('Yearly', 'Yearly'), ('Yearly Advance', 'Yearly Advance'),
    ]

    circuit_id = models.CharField(max_length=50, unique=True, editable=False)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES)

    # --- CROSS-APP LINKS ---
    dipl_pop_location = models.ForeignKey('app_core.PopLocation', on_delete=models.SET_NULL, null=True, verbose_name="DIPL POP Location")
    provider = models.ForeignKey('app_provider.Provider', on_delete=models.SET_NULL, null=True)
    circuit_type_obj = models.ForeignKey(CircuitType, on_delete=models.SET_NULL, null=True, verbose_name="Circuit Type")
    customer_name = models.ForeignKey('app_crm.Customer', on_delete=models.CASCADE, verbose_name="Customer Name")
    
    provider_circuit_id = models.CharField(max_length=100, blank=True, null=True)
    sub_customer = models.CharField(max_length=255, blank=True, null=True)
    bandwidth_value = models.IntegerField(default=0, verbose_name="Bandwidth Value")
    bandwidth_unit = models.CharField(max_length=10, choices=BANDWIDTH_UNIT_CHOICES, default='Mbps')

    po_date = models.DateField(blank=True, null=True)
    install_date = models.DateField(blank=True, null=True)
    test_done = models.BooleanField(default=False, verbose_name="Test Process Done")
    billing_date = models.DateField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    termination_reason = models.TextField(blank=True, null=True)

    customer_wan_ip = models.CharField(max_length=50, blank=True, null=True, verbose_name="Customer WAN IP")
    customer_lan_ip = models.CharField(max_length=50, blank=True, null=True, verbose_name="Customer LAN IP")

    tp_company_name = models.CharField(max_length=255, blank=True, null=True)
    tp_contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    tp_contact_person_no = models.CharField(max_length=20, blank=True, null=True)
    tp_location = models.CharField(max_length=255, blank=True, null=True)
    tp_media = models.CharField(max_length=20, choices=TP_MEDIA_CHOICES, blank=True, null=True)
    tp_billing_cycle = models.CharField(max_length=50, choices=TP_BILLING_CYCLE_CHOICES, blank=True, null=True)
    tp_billing_date = models.DateField(blank=True, null=True)
    sub_customer_address = models.TextField(blank=True, null=True)
    tp_termination_date = models.DateField(blank=True, null=True)
    tp_termination_reason = models.TextField(blank=True, null=True)

    is_closed = models.BooleanField(default=False, verbose_name="Fully Removed")
    attachment = models.FileField(upload_to='circuit_attachments/%Y/%m/%d/' , blank=True, null=True)
    attachment_name = models.CharField(max_length=255, blank=True, null=True, help_text="Original filename")
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.JSONField(default=list, blank=True, help_text="Store comments in JSON format")
    custom_data = models.JSONField(default=dict, blank=True, help_text="Stores dynamic drag-and-drop form data")
    activation_on_hold = models.BooleanField(default=False, verbose_name="Activation On Hold")
    activation_hold_reason = models.TextField(blank=True, null=True)
    deactivation_extension_days = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.circuit_id:
            import datetime
            current_year = datetime.datetime.now().year
            
            # --- DYNAMIC COMPANY PREFIX FETCHING ---
            from apps.app_core.models import CompanyProfile, SystemLog
            company = CompanyProfile.objects.first()
            prefix = company.short_code if company and company.short_code else "ISP"
            # ---------------------------------------

            base_prefix = f"{prefix}/CORE-BW/" if self.customer_type == 'CORE BW' else f"{prefix}/"
            year_prefix = f"{prefix}/CORE-BW/{current_year}/" if self.customer_type == 'CORE BW' else f"{prefix}/{current_year}/"

            used_nums = set()
            if self.customer_type == 'CORE BW':
                existing_ids = Circuit.objects.filter(circuit_id__startswith=base_prefix).values_list('circuit_id', flat=True)
            else:
                existing_ids = Circuit.objects.filter(circuit_id__startswith=base_prefix).exclude(circuit_id__startswith=f"{prefix}/CORE-BW/").values_list('circuit_id', flat=True)

            for cid in existing_ids:
                try: used_nums.add(int(cid.split('/')[-1]))
                except (ValueError, IndexError): pass

            # FETCHING SYSTEM LOG 
            if self.customer_type == 'CORE BW':
                log_ids = SystemLog.objects.filter(action='CREATE', model_type='Circuit', details__startswith=base_prefix).values_list('details', flat=True)
            else:
                log_ids = SystemLog.objects.filter(action='CREATE', model_type='Circuit', details__startswith=base_prefix).exclude(details__startswith=f"{prefix}/CORE-BW/").values_list('details', flat=True)

            for lid in log_ids:
                try: used_nums.add(int(lid.split('/')[-1]))
                except (ValueError, IndexError): pass

            next_num = 1
            while next_num in used_nums:
                next_num += 1

            self.circuit_id = f"{year_prefix}{next_num}" if self.customer_type == 'CORE BW' else f"{year_prefix}{next_num:04d}"

        super(Circuit, self).save(*args, **kwargs)

    def __str__(self): return self.circuit_id

class CircuitTenant(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='tenants')
    tenant_id = models.CharField(max_length=50, unique=True, editable=False)
    customer = models.ForeignKey('app_crm.Customer', on_delete=models.CASCADE)
    sub_customer = models.CharField(max_length=255, blank=True, null=True)
    bandwidth_value = models.IntegerField(default=0)
    bandwidth_unit = models.CharField(max_length=10, default='Mbps')
    billing_date = models.DateField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    termination_reason = models.TextField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    deactivation_extension_days = models.IntegerField(default=0)
    activation_on_hold = models.BooleanField(default=False, verbose_name="Activation On Hold")
    activation_hold_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            last_tenant = CircuitTenant.objects.filter(circuit=self.circuit).order_by('id').last()
            if last_tenant:
                try:
                    last_num = int(last_tenant.tenant_id.split('-')[-1])
                    next_num = last_num + 1
                except ValueError:
                    next_num = 2
            else:
                next_num = 2
            self.tenant_id = f"{self.circuit.circuit_id}-{next_num}"
        super().save(*args, **kwargs)

    def __str__(self): return f"{self.tenant_id} ({self.customer.customer_name})"

class CircuitTermination(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='terminations')
    end_type = models.CharField(max_length=1, choices=[('A', 'Termination A'), ('B', 'Termination B')])
    
    # --- CROSS-APP LINKS ---
    bts = models.ForeignKey('app_network.Bts', on_delete=models.CASCADE, verbose_name="Location / BTS")
    provider_network = models.ForeignKey('app_provider.ProviderNetwork', on_delete=models.SET_NULL, null=True, verbose_name="Telco Name")
    l2poi = models.ForeignKey('app_network.L2Poi', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="L2POI")

    SFP_CHOICES = [
        ('OTGB-100M', ' OTGB optical SFP 100M'), ('OTGB-1G',   ' OTGB optical SFP 1G'), ('OTGB-10G',  ' OTGB optical SFP 10G'),
        ('OTGB-25G',  ' OTGB optical SFP 25G'), ('OTGB-40G',  ' OTGB optical SFP 40G'), ('OTGB-100G', ' OTGB optical SFP 100G'),
        ('ETGB-100M', ' ETGB Copper SFP 100M'), ('ETGB-1G',   ' ETGB Copper SFP 1G'), ('ETGB-10G',  ' ETGB Copper SFP 10G'),
    ]
    sfp_type = models.CharField(max_length=50, choices=SFP_CHOICES, verbose_name="SFP Type / Speed")
    telco_bandwidth_value = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bandwidth Value")
    telco_bandwidth_unit = models.CharField(max_length=10, choices=[('Kbps', 'Kbps'), ('Mbps', 'Mbps'), ('Gbps', 'Gbps')], default='Mbps', verbose_name="Bandwidth Unit")
    connection_type = models.CharField(max_length=2, choices=[('L1', 'L1'), ('L2', 'L2')], default='L1')
    port_details = models.CharField(max_length=255, blank=True, null=True, verbose_name="Port Details")
    vlan_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="VLAN ID")
    ra_order_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="RA/Order No")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: unique_together = ('circuit', 'end_type')
    def __str__(self): return f"{self.get_end_type_display()} for {self.circuit}"

class CircuitAttachment(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='Circuit files/', blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-uploaded_at']

class BandwidthModification(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='bandwidth_modifications', null=True, blank=True)
    tenant = models.ForeignKey(CircuitTenant, on_delete=models.CASCADE, related_name='bandwidth_modifications', null=True, blank=True)
    mod_type = models.CharField(max_length=15, choices=[('Upgrade', 'Upgrade'), ('Downgrade', 'Downgrade')])
    old_value = models.IntegerField()
    old_unit = models.CharField(max_length=10)
    new_value = models.IntegerField()
    new_unit = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Hold', 'Hold'), ('Completed', 'Completed')], default='Pending')
    hold_reason = models.TextField(blank=True, null=True)
    new_telco_value = models.FloatField(null=True, blank=True)
    new_telco_unit = models.CharField(max_length=10, null=True, blank=True)
    old_telco_value = models.FloatField(null=True, blank=True)
    old_telco_unit = models.CharField(max_length=10, null=True, blank=True)
    telco_delta_value = models.FloatField(null=True, blank=True)
    telco_delta_unit = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class CircuitShifting(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='shiftings')
    termination = models.ForeignKey(CircuitTermination, on_delete=models.CASCADE, related_name='shiftings')
    
    # --- CROSS-APP LINKS ---
    new_bts = models.ForeignKey('app_network.Bts', on_delete=models.SET_NULL, null=True, verbose_name="New Location/BTS")
    new_provider_network = models.ForeignKey('app_provider.ProviderNetwork', on_delete=models.SET_NULL, null=True, blank=True)
    new_l2poi = models.ForeignKey('app_network.L2Poi', on_delete=models.SET_NULL, null=True, blank=True)
    
    new_sfp_type = models.CharField(max_length=50, blank=True, null=True)
    new_telco_bandwidth_value = models.CharField(max_length=50, blank=True, null=True)
    new_telco_bandwidth_unit = models.CharField(max_length=10, blank=True, null=True)
    new_connection_type = models.CharField(max_length=2, blank=True, null=True)
    new_port_details = models.CharField(max_length=255, blank=True, null=True)
    new_vlan_id = models.CharField(max_length=50, blank=True, null=True)
    new_ra_order_no = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Hold', 'Hold'), ('Completed', 'Completed')], default='Pending')
    hold_reason = models.TextField(blank=True, null=True)
    completion_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)