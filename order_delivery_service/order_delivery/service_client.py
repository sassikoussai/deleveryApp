"""
Service client for inter-service communication using Eureka service discovery
"""
import logging
import requests
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class ServiceClient:
    """Client for making HTTP requests to other microservices"""
    
    @staticmethod
    def get_user(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID from User Service
        
        Args:
            user_id: User ID
            
        Returns:
            User data dict or None if not found
        """
        try:
            from order_delivery.eureka_client import get_service_url
            
            service_url = get_service_url("USER-SERVICE")
            if not service_url:
                logger.error("USER-SERVICE not found in Eureka")
                return None
            
            # Spring Data REST endpoint format
            response = requests.get(f"{service_url}/users/{user_id}", timeout=5)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                logger.error(f"Error fetching user {user_id}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Exception fetching user {user_id}: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def get_restaurant(restaurant_id: int) -> Optional[Dict[str, Any]]:
        """
        Get restaurant by ID from Restaurant Service
        
        Args:
            restaurant_id: Restaurant ID
            
        Returns:
            Restaurant data dict or None if not found
        """
        try:
            from order_delivery.eureka_client import get_service_url
            
            service_url = get_service_url("RESTAURANTSERVICE")
            if not service_url:
                logger.error("RESTAURANTSERVICE not found in Eureka")
                return None
            
            # Spring Data REST endpoint format
            response = requests.get(f"{service_url}/restaurants/{restaurant_id}", timeout=5)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                logger.error(f"Error fetching restaurant {restaurant_id}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Exception fetching restaurant {restaurant_id}: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def get_restaurant_menu_items(restaurant_id: int) -> List[Dict[str, Any]]:
        """
        Get menu items for a restaurant
        
        Args:
            restaurant_id: Restaurant ID
            
        Returns:
            List of menu items
        """
        try:
            from order_delivery.eureka_client import get_service_url
            
            service_url = get_service_url("RESTAURANTSERVICE")
            if not service_url:
                logger.error("RESTAURANTSERVICE not found in Eureka")
                return []
            
            # Query menu items by restaurant ID
            response = requests.get(
                f"{service_url}/menu-items/search/findByRestaurantId",
                params={"restaurantId": restaurant_id},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                # Spring Data REST returns embedded resources
                if "_embedded" in data and "menuItems" in data["_embedded"]:
                    return data["_embedded"]["menuItems"]
                return []
            else:
                logger.error(f"Error fetching menu items for restaurant {restaurant_id}: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Exception fetching menu items for restaurant {restaurant_id}: {str(e)}", exc_info=True)
            return []

