from django.db import models
from django.core.validators import MinLengthValidator


class DeliveryStatus(models.TextChoices):
    ASSIGNED = 'ASSIGNED', 'Assigned'
    ON_THE_WAY = 'ON_THE_WAY', 'On The Way'
    DELIVERED = 'DELIVERED', 'Delivered'


class Delivery(models.Model):
    order_id = models.BigIntegerField(unique=True)
    courier_name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.ASSIGNED
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'deliveries'
        ordering = ['-assigned_at']

    def __str__(self):
        return f"Delivery {self.id} - Order {self.order_id} - {self.status}"

