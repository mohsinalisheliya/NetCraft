from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.app_circuit.models import Circuit
from apps.app_core.models import SystemLog
from apps.app_core.middleware import get_current_user # Apna jaadu import kiya

@receiver(post_save, sender=Circuit)
def log_circuit_save(sender, instance, created, **kwargs):
    user = get_current_user()
    
    # Agar API JWT se aayi hai, toh username milega, warna 'System' likha aayega
    username = user.username if user and user.is_authenticated else "System/Auto"
    
    action = 'CREATE' if created else 'UPDATE'
    details = f"Circuit {instance.circuit_id} has been {'created' if created else 'updated'}."
    
    # Chupke se SystemLog table mein entry daal di
    SystemLog.objects.create(
        username=username,
        action=action,
        model_type='Circuit',
        object_id=str(instance.circuit_id),
        details=details
    )

@receiver(post_delete, sender=Circuit)
def log_circuit_delete(sender, instance, **kwargs):
    user = get_current_user()
    username = user.username if user and user.is_authenticated else "System/Auto"
    
    SystemLog.objects.create(
        username=username,
        action='DELETE',
        model_type='Circuit',
        object_id=str(instance.circuit_id),
        details=f"Circuit {instance.circuit_id} has been deleted permanently."
    )