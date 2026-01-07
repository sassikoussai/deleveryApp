from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse
import time

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Business metrics
orders_created_total = Counter(
    'orders_created_total',
    'Total orders created',
    ['restaurant_id']
)

deliveries_created_total = Counter(
    'deliveries_created_total',
    'Total deliveries created',
    ['status']
)

active_orders = Gauge(
    'active_orders',
    'Number of active orders'
)

active_deliveries = Gauge(
    'active_deliveries',
    'Number of active deliveries',
    ['status']
)


def prometheus_metrics_view(request):
    """Expose Prometheus metrics"""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

