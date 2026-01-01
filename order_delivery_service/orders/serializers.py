from rest_framework import serializers
from .models import Order, OrderStatus
from order_delivery.service_client import ServiceClient


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices, required=False)
    user_details = serializers.SerializerMethodField()
    restaurant_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'restaurant_id', 'total_price', 'status', 'created_at', 
                  'user_details', 'restaurant_details']
        read_only_fields = ['id', 'created_at', 'user_details', 'restaurant_details']
    
    def get_user_details(self, obj):
        """Fetch user details from User Service"""
        user = ServiceClient.get_user(obj.user_id)
        if user:
            return {
                'id': user.get('id'),
                'firstName': user.get('firstName'),
                'lastName': user.get('lastName'),
                'email': user.get('email')
            }
        return None
    
    def get_restaurant_details(self, obj):
        """Fetch restaurant details from Restaurant Service"""
        restaurant = ServiceClient.get_restaurant(obj.restaurant_id)
        if restaurant:
            return {
                'id': restaurant.get('id'),
                'name': restaurant.get('name'),
                'address': restaurant.get('address'),
                'description': restaurant.get('description')
            }
        return None
    
    def create(self, validated_data):
        # Ensure status defaults to CREATED if not provided
        if 'status' not in validated_data:
            validated_data['status'] = OrderStatus.CREATED
        return super().create(validated_data)


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)

    def validate_status(self, value):
        if value == OrderStatus.CREATED:
            raise serializers.ValidationError("Cannot set status back to CREATED")
        return value

