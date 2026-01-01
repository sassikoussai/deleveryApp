package org.example.userservice;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import java.util.Optional;
import org.example.userservice.User;

@RepositoryRestResource(path = "users")
public interface UserRepo extends CrudRepository<User, Long> {
    Optional<User> findByEmail(String email); // Searching by email instead of username
}