from django.db import models

# 1. BTS Profile
class Bts(models.Model):
    name = models.CharField(max_length=255, verbose_name="BTS Name")
    code = models.CharField(max_length=100, verbose_name="BTS Code", unique=True)
    is_closed = models.BooleanField(default=False)
    address = models.TextField(verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
# 2. L2POI Profile (Linked across apps!)
class L2Poi(models.Model):
    CAPACITY_CHOICES = [
        ('1G', '1G'),
        ('10G', '10G'),
        ('25', '25G'),
        ('40G', '40G'),
        ('100G', '100G'),
    ]

    name = models.CharField(max_length=255, verbose_name="L2POI Name")
    
    # MAGIC: Accessing models from other apps using strings!
    provider_network = models.ForeignKey('app_provider.ProviderNetwork', on_delete=models.CASCADE, verbose_name="Provider Network") 
    customer = models.ForeignKey('app_crm.Customer', on_delete=models.CASCADE, verbose_name="Customer") 
    
    capacity = models.CharField(max_length=10, choices=CAPACITY_CHOICES, verbose_name="Type")
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.capacity}-{self.provider_network.name}-{self.customer.customer_name}"