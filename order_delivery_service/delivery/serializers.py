from rest_framework import serializers
from .models import Delivery, DeliveryStatus
from orders.services import OrderService


class DeliverySerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=DeliveryStatus.choices, required=False)
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = Delivery
        fields = ['id', 'order_id', 'courier_name', 'status', 'assigned_at', 'order_details']
        read_only_fields = ['id', 'assigned_at', 'order_details']
    
    def get_order_details(self, obj):
        """Fetch order details"""
        try:
            order = OrderService.get_order_by_id(obj.order_id)
            return {
                'id': order.id,
                'user_id': order.user_id,
                'restaurant_id': order.restaurant_id,
                'total_price': str(order.total_price),
                'status': order.status,
                'created_at': order.created_at.isoformat()
            }
        except Exception:
            return None
    
    def create(self, validated_data):
        # Ensure status defaults to ASSIGNED if not provided
        if 'status' not in validated_data:
            validated_data['status'] = DeliveryStatus.ASSIGNED
        return super().create(validated_data)


class DeliveryStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=DeliveryStatus.choices)

    def validate_status(self, value):
        if value == DeliveryStatus.ASSIGNED:
            raise serializers.ValidationError("Cannot set status back to ASSIGNED")
        return value

