from django.db import models

# 1. Provider Profile
class Provider(models.Model):
    provider = models.CharField(max_length=200, unique=True)
    address = models.TextField(verbose_name="Network Address", null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.provider

# 2. Provider Network Profile
class ProviderNetwork(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Provider")
    name = models.CharField(max_length=255, verbose_name="Network Name")
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.name}"