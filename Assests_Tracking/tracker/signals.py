from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CheckoutLog, Device


@receiver(post_save, sender=CheckoutLog)
def update_device_assigned_to(sender, instance, created, **kwargs):
    if created:
        instance.device.assigned_to = instance.employee
        instance.device.save()


@receiver(post_delete, sender=CheckoutLog)
def unset_device_assigned_to(sender, instance, **kwargs):
    instance.device.assigned_to = None
    instance.device.save()
