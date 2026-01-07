from django.core.management.base import BaseCommand
from orders.models import Order, OrderStatus
from delivery.models import Delivery, DeliveryStatus
from order_delivery.prometheus_metrics import active_orders, active_deliveries


class Command(BaseCommand):
    help = 'Update Prometheus metrics for active orders and deliveries'

    def handle(self, *args, **options):
        # Update active orders
        active_count = Order.objects.filter(
            status__in=[
                OrderStatus.CREATED,
                OrderStatus.CONFIRMED,
                OrderStatus.PREPARING,
                OrderStatus.DELIVERING
            ]
        ).count()
        active_orders.set(active_count)
        
        # Update active deliveries by status
        for status in [DeliveryStatus.ASSIGNED, DeliveryStatus.ON_THE_WAY]:
            count = Delivery.objects.filter(status=status).count()
            active_deliveries.labels(status=status).set(count)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated metrics: {active_count} active orders'
            )
        )

