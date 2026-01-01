from django.urls import path
from .views import (
    OrderCreateView,
    OrderDetailView,
    OrderListByUserView,
    OrderStatusUpdateView
)

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order-create'),
    path('user/<int:user_id>/', OrderListByUserView.as_view(), name='order-list-by-user'),
    path('<int:order_id>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]

