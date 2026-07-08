from django.db import models

class Customer(models.Model):
    ISP_CHOICES = [
        ('LICENCE', 'LICENCE'),
        ('CHANNEL-PARTNER', 'Channel-Partner'),
        ('CORPORATE', 'Corporate'),
    ]
    DOCUMENT_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField(blank=True, null=True)

    technical_name = models.CharField(max_length=150, verbose_name="Technical Person Name")
    technical_email = models.EmailField(verbose_name="Technical Email")
    technical_phone = models.CharField(max_length=15, verbose_name="Technical Phone")
    
    isp_type = models.CharField(max_length=15, choices=ISP_CHOICES, verbose_name="ISP Type")
    customer_document = models.CharField(max_length=3, choices=DOCUMENT_CHOICES, default='NO', verbose_name="Customer Document")

    billing_name = models.CharField(max_length=150, verbose_name="Billing Person Name")
    billing_contact_no = models.CharField(max_length=15, verbose_name="Billing Phone")
    billing_email = models.EmailField(verbose_name="Billing Email")
    gst_no = models.CharField(max_length=15, blank=True, null=True, verbose_name="GST Number")

    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name

    @property
    def has_active_links(self):
        if self.circuit_set.filter(is_closed=False).exists(): return True
        if self.circuittenant_set.filter(is_closed=False).exists(): return True
        if self.dxr_customers.filter(is_closed=False).exists(): return True
        if self.xconnect_a_ends.filter(is_closed=False).exists(): return True
        if self.xconnect_b_ends.filter(is_closed=False).exists(): return True
        return False

class CustomerAttachment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='customer files/', blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.file_name}"

    class Meta:
        ordering = ['-uploaded_at']