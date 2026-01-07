package org.example.restaurantservice;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import java.util.List;

@RepositoryRestResource(path = "menu-items")
public interface MenuItemRepo extends CrudRepository<MenuItem, Long> {
    
    // Query to find menu items by restaurant ID - using native query to check actual database
    @Query(value = "SELECT * FROM menu_item WHERE restaurant_id = :restaurantId", nativeQuery = true)
    List<MenuItem> findByRestaurantId(@Param("restaurantId") Long restaurantId);
}

