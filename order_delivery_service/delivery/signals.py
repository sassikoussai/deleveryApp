from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Delivery, DeliveryStatus
from order_delivery.prometheus_metrics import active_deliveries, deliveries_created_total


@receiver(post_save, sender=Delivery)
def update_delivery_metrics(sender, instance, created, **kwargs):
    """Update Prometheus metrics when a delivery is created or updated"""
    if created:
        # Increment counter when delivery is created
        deliveries_created_total.labels(status=instance.status).inc()
    
    # Update active deliveries gauge for all statuses
    for status in [DeliveryStatus.ASSIGNED, DeliveryStatus.ON_THE_WAY]:
        count = Delivery.objects.filter(status=status).count()
        active_deliveries.labels(status=status).set(count)


@receiver(post_delete, sender=Delivery)
def update_delivery_metrics_on_delete(sender, instance, **kwargs):
    """Update metrics when a delivery is deleted"""
    for status in [DeliveryStatus.ASSIGNED, DeliveryStatus.ON_THE_WAY]:
        count = Delivery.objects.filter(status=status).count()
        active_deliveries.labels(status=status).set(count)

