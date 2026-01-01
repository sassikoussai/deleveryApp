"""
Health check endpoint for Eureka service discovery
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    """
    Health check endpoint for Eureka
    GET /health/
    """
    def get(self, request):
        return Response({
            'status': 'UP',
            'service': 'order-delivery-service'
        }, status=status.HTTP_200_OK)

