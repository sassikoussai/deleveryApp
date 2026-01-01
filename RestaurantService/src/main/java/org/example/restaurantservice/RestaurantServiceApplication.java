package org.example.restaurantservice;

import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

@SpringBootApplication
public class RestaurantServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(RestaurantServiceApplication.class, args);
	}

	@Bean
	ApplicationRunner start(RestaurantRepo restaurantRepo, MenuItemRepo menuItemRepo) {
		return args -> {
			// Initializing the database with some restaurant data
			Restaurant pizzaHut = new Restaurant("Pizza Hut", "123 Pizza St, City", "Pizza, pasta, and more");
			Restaurant burgerKing = new Restaurant("Burger King", "456 Burger Rd, City", "Delicious burgers and fries");
			Restaurant tacoBell = new Restaurant("Taco Bell", "789 Taco Ave, City", "Tacos, burritos, and Mexican delights");
			
			// Save restaurants first
			pizzaHut = restaurantRepo.save(pizzaHut);
			burgerKing = restaurantRepo.save(burgerKing);
			tacoBell = restaurantRepo.save(tacoBell);
			
			// Add menu items for Pizza Hut
			List<MenuItem> pizzaHutMenu = Arrays.asList(
					new MenuItem("Margherita Pizza", "Classic tomato sauce, mozzarella, and basil", new BigDecimal("12.99"), "Main Course", pizzaHut),
					new MenuItem("Pepperoni Pizza", "Tomato sauce, mozzarella, and pepperoni", new BigDecimal("14.99"), "Main Course", pizzaHut),
					new MenuItem("Caesar Salad", "Fresh romaine lettuce with Caesar dressing", new BigDecimal("8.99"), "Appetizer", pizzaHut),
					new MenuItem("Garlic Bread", "Warm bread with garlic butter", new BigDecimal("5.99"), "Appetizer", pizzaHut),
					new MenuItem("Tiramisu", "Classic Italian dessert", new BigDecimal("6.99"), "Dessert", pizzaHut),
					new MenuItem("Coca Cola", "Refreshing soft drink", new BigDecimal("2.99"), "Beverage", pizzaHut)
			);
			menuItemRepo.saveAll(pizzaHutMenu);
			
			// Add menu items for Burger King
			List<MenuItem> burgerKingMenu = Arrays.asList(
					new MenuItem("Whopper", "Flame-grilled beef patty with fresh vegetables", new BigDecimal("7.99"), "Main Course", burgerKing),
					new MenuItem("Chicken Royale", "Crispy chicken fillet with special sauce", new BigDecimal("6.99"), "Main Course", burgerKing),
					new MenuItem("French Fries", "Golden crispy fries", new BigDecimal("3.99"), "Side", burgerKing),
					new MenuItem("Onion Rings", "Crispy battered onion rings", new BigDecimal("4.99"), "Side", burgerKing),
					new MenuItem("Chocolate Shake", "Creamy chocolate milkshake", new BigDecimal("4.99"), "Beverage", burgerKing),
					new MenuItem("Apple Pie", "Warm apple pie dessert", new BigDecimal("2.99"), "Dessert", burgerKing)
			);
			menuItemRepo.saveAll(burgerKingMenu);
			
			// Add menu items for Taco Bell
			List<MenuItem> tacoBellMenu = Arrays.asList(
					new MenuItem("Crunchy Taco", "Seasoned beef, lettuce, and cheese in a crunchy shell", new BigDecimal("2.99"), "Main Course", tacoBell),
					new MenuItem("Bean Burrito", "Refried beans, red sauce, and cheese", new BigDecimal("3.99"), "Main Course", tacoBell),
					new MenuItem("Nachos Supreme", "Tortilla chips with beef, beans, cheese, and sour cream", new BigDecimal("5.99"), "Appetizer", tacoBell),
					new MenuItem("Quesadilla", "Melted cheese in a grilled tortilla", new BigDecimal("4.99"), "Main Course", tacoBell),
					new MenuItem("Cinnamon Twists", "Sweet cinnamon dessert", new BigDecimal("1.99"), "Dessert", tacoBell),
					new MenuItem("Mountain Dew", "Citrus-flavored soft drink", new BigDecimal("2.49"), "Beverage", tacoBell)
			);
			menuItemRepo.saveAll(tacoBellMenu);
		};
	}
}
