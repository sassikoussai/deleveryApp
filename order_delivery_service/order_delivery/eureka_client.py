"""
Eureka client registration for Django service
"""
import os
import logging
import atexit
import requests
from py_eureka_client import eureka_client

logger = logging.getLogger(__name__)

# Eureka client instance
eureka_client_instance = None


def register_with_eureka():
    """
    Register this Django service with Eureka server
    """
    global eureka_client_instance
    
    try:
        # Get configuration from Django settings
        # Use try-except to handle cases where Django might not be fully initialized
        try:
            from django.conf import settings
            eureka_enabled = getattr(settings, 'EUREKA_ENABLED', True)
            if not eureka_enabled:
                logger.info("Eureka registration is disabled in settings")
                return
        except Exception:
            # Django not initialized yet, use defaults
            logger.warning("Django settings not available, using default Eureka configuration")
        
        eureka_server_url = os.environ.get('EUREKA_SERVER_URL', 'http://localhost:8761/eureka')
        app_name = os.environ.get('EUREKA_APP_NAME', 'ORDER-DELIVERY-SERVICE')  # Must match gateway service ID
        instance_host = os.environ.get('EUREKA_INSTANCE_HOST', 'localhost')
        instance_port = int(os.environ.get('EUREKA_INSTANCE_PORT', '8000'))
        instance_ip = os.environ.get('EUREKA_INSTANCE_IP', '127.0.0.1')
        
        # Try to get from Django settings if available
        try:
            from django.conf import settings
            eureka_server_url = getattr(settings, 'EUREKA_SERVER_URL', eureka_server_url)
            app_name = getattr(settings, 'EUREKA_APP_NAME', app_name)
            instance_host = getattr(settings, 'EUREKA_INSTANCE_HOST', instance_host)
            instance_port = getattr(settings, 'EUREKA_INSTANCE_PORT', instance_port)
            instance_ip = getattr(settings, 'EUREKA_INSTANCE_IP', instance_ip)
        except Exception:
            pass  # Use environment variables or defaults
        
        logger.info(f"Registering {app_name} with Eureka at {eureka_server_url}")
        logger.info(f"Instance details: host={instance_host}, port={instance_port}, ip={instance_ip}")
        
        # Register with Eureka
        eureka_client.init(
            eureka_server=eureka_server_url,
            app_name=app_name,
            instance_host=instance_host,
            instance_port=instance_port,
            instance_ip=instance_ip,
            renewal_interval_in_secs=30,
            duration_in_secs=90,
            # Health check URL (optional)
            health_check_url=f"http://{instance_ip}:{instance_port}/health/",
            # Home page URL
            home_page_url=f"http://{instance_ip}:{instance_port}/",
        )
        
        eureka_client_instance = eureka_client
        logger.info(f"Successfully registered {app_name} with Eureka")
        logger.info(f"Service should be available at: http://{instance_ip}:{instance_port}")
        
        # Register cleanup function to unregister on exit
        atexit.register(unregister_from_eureka)
        
    except Exception as e:
        logger.error(f"Failed to register with Eureka: {str(e)}", exc_info=True)


def unregister_from_eureka():
    """
    Unregister this service from Eureka server
    """
    global eureka_client_instance
    
    try:
        if eureka_client_instance:
            eureka_client.stop()
            logger.info("Successfully unregistered from Eureka")
    except Exception as e:
        logger.error(f"Failed to unregister from Eureka: {str(e)}", exc_info=True)


def get_service_url(service_name):
    """
    Get the URL of a service registered with Eureka
    
    Args:
        service_name: Name of the service to discover
        
    Returns:
        Service URL or None if not found
    """
    try:
        # Try using py-eureka-client's get_app method
        try:
            app = eureka_client.get_app(service_name)
            if app and hasattr(app, 'instances') and app.instances:
                # Get the first available instance
                instance = app.instances[0]
                # Handle both port as object and port as integer
                port = instance.port.port if hasattr(instance.port, 'port') else instance.port
                ip_addr = instance.ipAddr if hasattr(instance, 'ipAddr') else instance.ip
                return f"http://{ip_addr}:{port}"
        except AttributeError:
            # If get_app doesn't work, fall back to Eureka REST API
            pass
        
        # Fallback: Query Eureka REST API directly
        eureka_server_url = os.environ.get('EUREKA_SERVER_URL', 'http://localhost:8761/eureka')
        # Remove /eureka suffix if present for REST API calls
        eureka_base = eureka_server_url.replace('/eureka', '')
        
        # Query Eureka REST API for the app
        response = requests.get(
            f"{eureka_base}/eureka/apps/{service_name}",
            headers={'Accept': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            # Eureka REST API returns: {"application": {"instance": [...]}}
            if 'application' in data and 'instance' in data['application']:
                instances = data['application']['instance']
                if instances:
                    # Get first instance (handle both single instance and list)
                    if isinstance(instances, list):
                        instance = instances[0]
                    else:
                        instance = instances
                    
                    ip_addr = instance.get('ipAddr') or instance.get('ip')
                    port_info = instance.get('port', {})
                    port = port_info.get('$') if isinstance(port_info, dict) else port_info
                    
                    if ip_addr and port:
                        return f"http://{ip_addr}:{port}"
        
        return None
    except Exception as e:
        logger.error(f"Failed to discover service {service_name}: {str(e)}", exc_info=True)
        return None

