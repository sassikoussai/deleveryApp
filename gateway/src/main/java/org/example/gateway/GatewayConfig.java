package org.example.gateway;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsWebFilter;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                // User Service Route
                .route("user-service", r -> r
                        .path("/api/users/**")
                        .filters(f -> f.stripPrefix(1))
                        .uri("lb://USER-SERVICE"))
                
                // Menu Items Route (must come before restaurants to match first)
                .route("menu-items-service", r -> r
                        .path("/api/restaurants/menu-items/**")
                        .filters(f -> f.rewritePath("/api/restaurants/menu-items/(?<segment>.*)", "/menu-items/${segment}"))
                        .uri("lb://RESTAURANTSERVICE"))
                
                // Restaurant Service Route
                .route("restaurant-service", r -> r
                        .path("/api/restaurants/**")
                        .filters(f -> f.stripPrefix(1))
                        .uri("lb://RESTAURANTSERVICE"))
                
                // Order Service Route - DON'T strip prefix (Django has /api/ in paths)
                .route("order-service", r -> r
                        .path("/api/orders/**")
                        .uri("lb://ORDER-DELIVERY-SERVICE"))
                
                // Delivery Service Route - DON'T strip prefix (Django has /api/ in paths)
                .route("delivery-service", r -> r
                        .path("/api/deliveries/**")
                        .uri("lb://ORDER-DELIVERY-SERVICE"))
                
                .build();
    }

    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration corsConfig = new CorsConfiguration();
        // Allow all origins including null (for file:// protocol)
        corsConfig.setAllowedOriginPatterns(Arrays.asList("*")); 
        corsConfig.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));
        corsConfig.setAllowedHeaders(Arrays.asList("*"));
        corsConfig.setAllowCredentials(false); // Must be false when using wildcard patterns
        corsConfig.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);

        return new CorsWebFilter(source);
    }
}

