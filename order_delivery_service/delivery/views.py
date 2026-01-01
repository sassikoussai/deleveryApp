from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .serializers import DeliverySerializer, DeliveryStatusUpdateSerializer
from .services import DeliveryService


class DeliveryCreateView(APIView):
    """
    POST /api/deliveries/
    Create a new delivery.
    """
    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            try:
                delivery = DeliveryService.create_delivery(
                    order_id=serializer.validated_data['order_id'],
                    courier_name=serializer.validated_data['courier_name']
                )
                response_serializer = DeliverySerializer(delivery)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryDetailView(APIView):
    """
    GET /api/deliveries/{id}/
    Get delivery by ID.
    """
    def get(self, request, delivery_id):
        try:
            delivery = DeliveryService.get_delivery_by_id(delivery_id)
            serializer = DeliverySerializer(delivery)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class DeliveryByOrderView(APIView):
    """
    GET /api/deliveries/order/{order_id}/
    Get delivery by order ID.
    """
    def get(self, request, order_id):
        try:
            delivery = DeliveryService.get_delivery_by_order(order_id)
            serializer = DeliverySerializer(delivery)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class DeliveryStatusUpdateView(APIView):
    """
    PUT /api/deliveries/{id}/status/
    Update delivery status.
    """
    def put(self, request, delivery_id):
        serializer = DeliveryStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                delivery = DeliveryService.update_delivery_status(
                    delivery_id=delivery_id,
                    new_status=serializer.validated_data['status']
                )
                response_serializer = DeliverySerializer(delivery)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except NotFound as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

