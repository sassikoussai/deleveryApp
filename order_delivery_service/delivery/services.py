from rest_framework.exceptions import NotFound, ValidationError as DRFValidationError
from .models import Delivery, DeliveryStatus
from orders.services import OrderService
from order_delivery.prometheus_metrics import deliveries_created_total, active_deliveries


class DeliveryService:
    @staticmethod
    def create_delivery(order_id, courier_name):
        """
        Create a new delivery with order validation.
        
        Args:
            order_id: ID of the order to deliver
            courier_name: Name of the courier
            
        Returns:
            Delivery instance
            
        Raises:
            DRFValidationError: If validation fails
        """
        if order_id <= 0:
            raise DRFValidationError({"order_id": "Order ID must be a positive integer"})
        
        if not courier_name or not courier_name.strip():
            raise DRFValidationError({"courier_name": "Courier name cannot be empty"})
        
        # Validate order exists
        try:
            order = OrderService.get_order_by_id(order_id)
        except NotFound:
            raise DRFValidationError({"order_id": f"Order with id {order_id} does not exist"})
        
        # Check if delivery already exists for this order
        if Delivery.objects.filter(order_id=order_id).exists():
            raise DRFValidationError({"order_id": "Delivery already exists for this order"})
        
        delivery = Delivery.objects.create(
            order_id=order_id,
            courier_name=courier_name.strip(),
            status=DeliveryStatus.ASSIGNED
        )
        # Increment Prometheus metrics
        deliveries_created_total.labels(status=DeliveryStatus.ASSIGNED).inc()
        # Update active deliveries gauge
        for status in [DeliveryStatus.ASSIGNED, DeliveryStatus.ON_THE_WAY]:
            count = Delivery.objects.filter(status=status).count()
            active_deliveries.labels(status=status).set(count)
        return delivery

    @staticmethod
    def get_delivery_by_id(delivery_id):
        """
        Get delivery by ID.
        
        Args:
            delivery_id: ID of the delivery
            
        Returns:
            Delivery instance
            
        Raises:
            NotFound: If delivery does not exist
        """
        try:
            return Delivery.objects.get(id=delivery_id)
        except Delivery.DoesNotExist:
            raise NotFound(f"Delivery with id {delivery_id} not found")

    @staticmethod
    def get_delivery_by_order(order_id):
        """
        Get delivery by order ID.
        
        Args:
            order_id: ID of the order
            
        Returns:
            Delivery instance
            
        Raises:
            NotFound: If delivery does not exist
        """
        try:
            return Delivery.objects.get(order_id=order_id)
        except Delivery.DoesNotExist:
            raise NotFound(f"Delivery for order {order_id} not found")

    @staticmethod
    def update_delivery_status(delivery_id, new_status):
        """
        Update delivery status.
        
        Args:
            delivery_id: ID of the delivery
            new_status: New status value
            
        Returns:
            Delivery instance
            
        Raises:
            NotFound: If delivery does not exist
            DRFValidationError: If status transition is invalid
        """
        try:
            delivery = Delivery.objects.get(id=delivery_id)
        except Delivery.DoesNotExist:
            raise NotFound(f"Delivery with id {delivery_id} not found")
        
        # Validate status transition
        valid_transitions = {
            DeliveryStatus.ASSIGNED: [DeliveryStatus.ON_THE_WAY],
            DeliveryStatus.ON_THE_WAY: [DeliveryStatus.DELIVERED],
            DeliveryStatus.DELIVERED: [],  # Final state
        }
        
        current_status = delivery.status
        if new_status not in valid_transitions.get(current_status, []):
            raise DRFValidationError(
                f"Cannot transition from {current_status} to {new_status}"
            )
        
        delivery.status = new_status
        delivery.save()
        # Update active deliveries gauge
        for status in [DeliveryStatus.ASSIGNED, DeliveryStatus.ON_THE_WAY]:
            count = Delivery.objects.filter(status=status).count()
            active_deliveries.labels(status=status).set(count)
        return delivery

