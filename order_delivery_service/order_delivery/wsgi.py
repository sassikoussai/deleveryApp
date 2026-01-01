"""
WSGI config for order_delivery project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_delivery.settings')

application = get_wsgi_application()

# Register with Eureka after Django is fully loaded
logger = logging.getLogger(__name__)
try:
    from django.conf import settings
    if getattr(settings, 'EUREKA_ENABLED', True):
        from order_delivery.eureka_client import register_with_eureka
        register_with_eureka()
        logger.info("Eureka registration initiated from WSGI")
except Exception as e:
    logger.error(f"Failed to register with Eureka: {str(e)}", exc_info=True)

