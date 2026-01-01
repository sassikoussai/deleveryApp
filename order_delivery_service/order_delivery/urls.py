"""
URL configuration for order_delivery project.
"""
from django.contrib import admin
from django.urls import path, include
from .health_views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('api/orders/', include('orders.urls')),
    path('api/deliveries/', include('delivery.urls')),
]

