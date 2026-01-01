package org.example.userservice;

import org.example.userservice.User;
import org.example.userservice.UserRepo;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.stream.Stream;


@SpringBootApplication
public class UserServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }

    @Bean
    ApplicationRunner start(UserRepo userRepo) {
        return args -> {
            Stream.of(
                    new User("John", "Doe", "john.doe@example.com"),
                    new User("Jane", "Smith", "jane.smith@example.com"),
                    new User("Bob", "Johnson", "bob.johnson@example.com")
            ).forEach(userRepo::save);
        };
    }
}
