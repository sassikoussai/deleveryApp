from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderStatus
from order_delivery.prometheus_metrics import active_orders, orders_created_total


@receiver(post_save, sender=Order)
def update_order_metrics(sender, instance, created, **kwargs):
    """Update Prometheus metrics when an order is created or updated"""
    if created:
        # Increment counter when order is created
        orders_created_total.labels(restaurant_id=str(instance.restaurant_id)).inc()
    
    # Update active orders gauge
    active_count = Order.objects.filter(
        status__in=[
            OrderStatus.CREATED,
            OrderStatus.CONFIRMED,
            OrderStatus.PREPARING,
            OrderStatus.DELIVERING
        ]
    ).count()
    active_orders.set(active_count)


@receiver(post_delete, sender=Order)
def update_order_metrics_on_delete(sender, instance, **kwargs):
    """Update metrics when an order is deleted"""
    active_count = Order.objects.filter(
        status__in=[
            OrderStatus.CREATED,
            OrderStatus.CONFIRMED,
            OrderStatus.PREPARING,
            OrderStatus.DELIVERING
        ]
    ).count()
    active_orders.set(active_count)

