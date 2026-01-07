from django.utils.deprecation import MiddlewareMixin
from .prometheus_metrics import http_requests_total, http_request_duration_seconds
import time


class PrometheusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._prometheus_start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_prometheus_start_time'):
            duration = time.time() - request._prometheus_start_time
            method = request.method
            endpoint = request.path
            status = response.status_code

            http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

        return response

