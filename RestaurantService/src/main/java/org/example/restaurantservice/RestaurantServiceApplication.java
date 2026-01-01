package org.example.restaurantservice;

import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.stream.Stream;

@SpringBootApplication
public class RestaurantServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(RestaurantServiceApplication.class, args);
	}

	@Bean
	ApplicationRunner start(RestaurantRepo restaurantRepo) {
		return args -> {
			// Initializing the database with some restaurant data
			Stream.of(
					new Restaurant("Pizza Hut", "123 Pizza St, City", "Pizza, pasta, and more"),
					new Restaurant("Burger King", "456 Burger Rd, City", "Delicious burgers and fries"),
					new Restaurant("Taco Bell", "789 Taco Ave, City", "Tacos, burritos, and Mexican delights")
			).forEach(restaurantRepo::save);  // Save to the database
		};
	}
}
