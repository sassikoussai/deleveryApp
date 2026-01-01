package org.example.restaurantservice;


import org.springframework.data.repository.CrudRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import java.util.Optional;

@RepositoryRestResource(path = "restaurants")
public interface RestaurantRepo extends CrudRepository<Restaurant, Long> {

    // Custom query to find a restaurant by name
    Optional<Restaurant> findByName(String name);
}
