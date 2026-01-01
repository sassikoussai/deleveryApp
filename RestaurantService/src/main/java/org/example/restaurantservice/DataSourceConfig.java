package org.example.restaurantservice;

import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import javax.sql.DataSource;
import java.sql.DriverManager;

@Configuration
public class DataSourceConfig {

    @Bean
    @Primary
    public DataSource dataSource() {
        // Explicitly load SQLite driver using system classloader (NOT RestartClassLoader)
        // This ensures HikariCP can find the driver class even with DevTools active
        try {
            ClassLoader systemClassLoader = ClassLoader.getSystemClassLoader();
            Class<?> driverClass = systemClassLoader.loadClass("org.sqlite.JDBC");
            // Register the driver with DriverManager so HikariCP can find it
            DriverManager.registerDriver((java.sql.Driver) driverClass.getDeclaredConstructor().newInstance());
        } catch (Exception e) {
            // If system classloader fails, try the context classloader (but not Class.forName which uses RestartClassLoader)
            try {
                ClassLoader contextClassLoader = Thread.currentThread().getContextClassLoader();
                if (contextClassLoader != null && contextClassLoader != ClassLoader.getSystemClassLoader()) {
                    Class<?> driverClass = contextClassLoader.loadClass("org.sqlite.JDBC");
                    DriverManager.registerDriver((java.sql.Driver) driverClass.getDeclaredConstructor().newInstance());
                } else {
                    throw new RuntimeException("SQLite JDBC driver not found. Make sure sqlite-jdbc dependency is included.", e);
                }
            } catch (Exception ex) {
                throw new RuntimeException("SQLite JDBC driver not found. Make sure sqlite-jdbc dependency is included.", ex);
            }
        }
        
        return DataSourceBuilder.create()
                .driverClassName("org.sqlite.JDBC")
                .url("jdbc:sqlite:restaurant_service.db")
                .build();
    }
}

