from django.db import models


class OrderStatus(models.TextChoices):
    CREATED = 'CREATED', 'Created'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    PREPARING = 'PREPARING', 'Preparing'
    DELIVERING = 'DELIVERING', 'Delivering'
    DELIVERED = 'DELIVERED', 'Delivered'
    CANCELED = 'CANCELED', 'Canceled'


class Order(models.Model):
    user_id = models.BigIntegerField()
    restaurant_id = models.BigIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - User {self.user_id} - {self.status}"

