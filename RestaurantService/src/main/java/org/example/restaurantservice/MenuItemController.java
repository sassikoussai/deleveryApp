package org.example.restaurantservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@RestController
public class MenuItemController {

    @Autowired
    private MenuItemRepo menuItemRepo;

    @Autowired
    private RestaurantRepo restaurantRepo;

    @GetMapping("/debug/menu-items")
    public ResponseEntity<?> debugMenuItems() {
        // Debug: Show all menu items with their restaurant IDs
        List<MenuItem> allItems = (List<MenuItem>) menuItemRepo.findAll();
        java.util.Map<String, Object> debug = new java.util.HashMap<>();
        debug.put("totalItems", allItems.size());
        java.util.List<java.util.Map<String, Object>> itemsInfo = new java.util.ArrayList<>();
        for (MenuItem item : allItems) {
            java.util.Map<String, Object> info = new java.util.HashMap<>();
            info.put("id", item.getId());
            info.put("name", item.getName());
            info.put("restaurantId", item.getRestaurant() != null ? item.getRestaurant().getId() : "NULL");
            info.put("restaurant", item.getRestaurant() != null ? item.getRestaurant().getName() : "NULL");
            itemsInfo.add(info);
        }
        debug.put("items", itemsInfo);
        return ResponseEntity.ok(debug);
    }

    @GetMapping("/menu-items/by-restaurant/{restaurantId}")
    public ResponseEntity<?> getMenuItemsByRestaurant(@PathVariable Long restaurantId) {
        // Get ALL menu items first
        List<MenuItem> allItems = (List<MenuItem>) menuItemRepo.findAll();
        
        // Debug: print what we have
        System.out.println("=== DEBUG: Total items in DB: " + allItems.size());
        for (MenuItem item : allItems) {
            System.out.println("Item ID: " + item.getId() + ", Name: " + item.getName() + 
                ", Restaurant: " + (item.getRestaurant() != null ? item.getRestaurant().getId() : "NULL"));
        }
        
        // Filter by restaurant ID
        List<MenuItem> filtered = new java.util.ArrayList<>();
        for (MenuItem item : allItems) {
            if (item.getRestaurant() != null && item.getRestaurant().getId().equals(restaurantId)) {
                filtered.add(item);
            }
        }
        
        System.out.println("=== DEBUG: Filtered items for restaurant " + restaurantId + ": " + filtered.size());
        return ResponseEntity.ok(filtered);
    }

    @PostMapping("/menu-items")
    public ResponseEntity<?> createMenuItem(@RequestBody MenuItemRequest request) {
        try {
            System.out.println("=== CREATE MENU ITEM DEBUG ===");
            System.out.println("Received restaurantId: " + request.getRestaurantId());
            System.out.println("Name: " + request.getName());
            
            Optional<Restaurant> restaurantOpt = restaurantRepo.findById(request.getRestaurantId());
            if (restaurantOpt.isEmpty()) {
                System.out.println("ERROR: Restaurant not found: " + request.getRestaurantId());
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Restaurant with ID " + request.getRestaurantId() + " not found");
            }

            MenuItem menuItem = new MenuItem();
            menuItem.setName(request.getName());
            menuItem.setDescription(request.getDescription());
            menuItem.setPrice(new BigDecimal(request.getPrice()));
            menuItem.setCategory(request.getCategory());
            menuItem.setRestaurant(restaurantOpt.get());

            MenuItem saved = menuItemRepo.save(menuItem);
            System.out.println("SUCCESS: Saved menu item ID: " + saved.getId() + ", Restaurant ID: " + saved.getRestaurant().getId());
            return ResponseEntity.status(HttpStatus.CREATED).body(saved);
        } catch (Exception e) {
            System.out.println("ERROR creating menu item: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body("Error creating menu item: " + e.getMessage());
        }
    }

    public static class MenuItemRequest {
        private Long restaurantId;
        private String name;
        private String description;
        private String price;
        private String category;

        public Long getRestaurantId() { return restaurantId; }
        public void setRestaurantId(Long restaurantId) { this.restaurantId = restaurantId; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public String getPrice() { return price; }
        public void setPrice(String price) { this.price = price; }
        public String getCategory() { return category; }
        public void setCategory(String category) { this.category = category; }
    }
}

