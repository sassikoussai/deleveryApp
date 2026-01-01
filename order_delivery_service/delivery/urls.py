from django.urls import path
from .views import (
    DeliveryCreateView,
    DeliveryDetailView,
    DeliveryByOrderView,
    DeliveryStatusUpdateView
)

urlpatterns = [
    path('', DeliveryCreateView.as_view(), name='delivery-create'),
    path('<int:delivery_id>/', DeliveryDetailView.as_view(), name='delivery-detail'),
    path('order/<int:order_id>/', DeliveryByOrderView.as_view(), name='delivery-by-order'),
    path('<int:delivery_id>/status/', DeliveryStatusUpdateView.as_view(), name='delivery-status-update'),
]

