from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from .services import OrderService


class OrderCreateView(APIView):
    """
    POST /api/orders/
    Create a new order.
    """
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = OrderService.create_order(
                    user_id=serializer.validated_data['user_id'],
                    restaurant_id=serializer.validated_data['restaurant_id'],
                    total_price=serializer.validated_data['total_price']
                )
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """
    GET /api/orders/{id}/
    Get order by ID.
    """
    def get(self, request, order_id):
        try:
            order = OrderService.get_order_by_id(order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class OrderListByUserView(APIView):
    """
    GET /api/orders/user/{user_id}/
    List all orders for a specific user.
    """
    def get(self, request, user_id):
        orders = OrderService.get_orders_by_user(user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderStatusUpdateView(APIView):
    """
    PUT /api/orders/{id}/status/
    Update order status.
    """
    def put(self, request, order_id):
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = OrderService.update_order_status(
                    order_id=order_id,
                    new_status=serializer.validated_data['status']
                )
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except NotFound as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

