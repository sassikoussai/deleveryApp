from rest_framework.exceptions import NotFound, ValidationError as DRFValidationError
from .models import Order, OrderStatus
from order_delivery.service_client import ServiceClient


class OrderService:
    @staticmethod
    def create_order(user_id, restaurant_id, total_price):
        """
        Create a new order with validation.
        
        Args:
            user_id: ID of the user placing the order
            restaurant_id: ID of the restaurant
            total_price: Total price of the order
            
        Returns:
            Order instance
            
        Raises:
            DRFValidationError: If validation fails
        """
        if total_price <= 0:
            raise DRFValidationError({"total_price": "Total price must be greater than 0"})
        
        if user_id <= 0:
            raise DRFValidationError({"user_id": "User ID must be a positive integer"})
        
        if restaurant_id <= 0:
            raise DRFValidationError({"restaurant_id": "Restaurant ID must be a positive integer"})
        
        # Validate user exists
        user = ServiceClient.get_user(user_id)
        if not user:
            raise DRFValidationError({"user_id": f"User with id {user_id} does not exist"})
        
        # Validate restaurant exists
        restaurant = ServiceClient.get_restaurant(restaurant_id)
        if not restaurant:
            raise DRFValidationError({"restaurant_id": f"Restaurant with id {restaurant_id} does not exist"})
        
        order = Order.objects.create(
            user_id=user_id,
            restaurant_id=restaurant_id,
            total_price=total_price,
            status=OrderStatus.CREATED
        )
        return order

    @staticmethod
    def get_order_by_id(order_id):
        """
        Get order by ID.
        
        Args:
            order_id: ID of the order
            
        Returns:
            Order instance
            
        Raises:
            NotFound: If order does not exist
        """
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(f"Order with id {order_id} not found")

    @staticmethod
    def get_orders_by_user(user_id):
        """
        Get all orders for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            QuerySet of Order instances
        """
        return Order.objects.filter(user_id=user_id)

    @staticmethod
    def update_order_status(order_id, new_status):
        """
        Update order status.
        
        Args:
            order_id: ID of the order
            new_status: New status value
            
        Returns:
            Order instance
            
        Raises:
            NotFound: If order does not exist
            DRFValidationError: If status transition is invalid
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(f"Order with id {order_id} not found")
        
        # Validate status transition
        valid_transitions = {
            OrderStatus.CREATED: [OrderStatus.CONFIRMED, OrderStatus.CANCELED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELED],
            OrderStatus.PREPARING: [OrderStatus.DELIVERING, OrderStatus.CANCELED],
            OrderStatus.DELIVERING: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],  # Final state
            OrderStatus.CANCELED: [],  # Final state
        }
        
        current_status = order.status
        if new_status not in valid_transitions.get(current_status, []):
            raise DRFValidationError(
                f"Cannot transition from {current_status} to {new_status}"
            )
        
        order.status = new_status
        order.save()
        return order

