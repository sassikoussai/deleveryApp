from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'courier_name', 'status', 'assigned_at']
    list_filter = ['status', 'assigned_at']
    search_fields = ['order_id', 'courier_name']

