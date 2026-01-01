package org.example.restaurantservice;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import java.util.List;

@RepositoryRestResource(path = "menu-items")
public interface MenuItemRepo extends CrudRepository<MenuItem, Long> {
    
    // Find all menu items for a specific restaurant
    List<MenuItem> findByRestaurantId(Long restaurantId);
    
    // Find menu items by category for a restaurant
    List<MenuItem> findByRestaurantIdAndCategory(Long restaurantId, String category);
    
    // Find menu items by restaurant name
    List<MenuItem> findByRestaurantName(String restaurantName);
}

