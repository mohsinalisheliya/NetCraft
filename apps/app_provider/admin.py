from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = admin.site.site_title = "NetCraft"

all_models = [
   Provider,
   ProviderNetwork,
] 

for model in all_models:
    admin.site.register(model)